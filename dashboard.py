
import csv
import json
import math
import tkinter as tk

from pathlib import Path
from tkinter import ttk, messagebox, simpledialog

from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys

from rexpilot.dino_controller import DinoController
from rexpilot.session_manager import SessionManager
from rexpilot.performance_logger import PerformanceLogger

from rexpilot.conservative_strategy import ConservativeStrategy
from rexpilot.balanced_strategy import BalancedStrategy
from rexpilot.aggressive_strategy import AggressiveStrategy


class RexPilotDashboard:

    STRATEGIES = {
        "Conservative": ConservativeStrategy,
        "Balanced": BalancedStrategy,
        "Aggressive": AggressiveStrategy
    }

    PARAMETERS = [
        "jump_duration",
        "duck_duration",
        "delay_between_actions",
        "waiting_interval",
        "session_duration"
    ]

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("RexPilot - Performance Dashboard")
        self.root.geometry("900x750")
        self.root.minsize(780, 650)

        self.config_path = (
            Path(__file__).resolve().parent / "config.json"
        )

        # Core components
        self.manager = SessionManager()
        self.logger = PerformanceLogger()
        self.controller = DinoController()

        # Configuration
        self.config = self.load_config()

        # Session state
        self.current_session = None
        self.last_duration = 0.0

        # Automation scheduler state
        self.action_job = None
        self.next_action = "jump"

        # Dashboard data
        self.parameter_vars = {}
        self.history_scores = []
        self.history_count = 0

        # Build interface
        self.build_interface()

        # Restore previous session records
        self.load_history()

        # Start dashboard timer
        self.update_timer()

        # Handle window closure
        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_dashboard
        )

    # --------------------------------------------------
    # CONFIGURATION
    # --------------------------------------------------

    def load_config(self):

        if not self.config_path.exists():
            raise FileNotFoundError(
                "config.json was not found in the project directory."
            )

        try:

            with open(
                self.config_path,
                "r",
                encoding="utf-8"
            ) as file:

                config = json.load(file)

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Invalid JSON configuration: {error}"
            ) from error

        if not isinstance(config, dict):
            raise ValueError(
                "Configuration must be a JSON object."
            )

        strategy_name = config.get("selected_strategy")

        if strategy_name not in self.STRATEGIES:
            raise ValueError(
                f"Unknown selected strategy: {strategy_name}"
            )

        strategies = config.get("strategies")

        if not isinstance(strategies, dict):
            raise ValueError(
                "The strategies section is missing or invalid."
            )

        for name in self.STRATEGIES:

            parameters = strategies.get(name)

            if not isinstance(parameters, dict):
                raise ValueError(
                    f"Configuration for {name} is missing."
                )

            for parameter in self.PARAMETERS:

                if parameter not in parameters:
                    raise ValueError(
                        f"{parameter} is missing from {name} configuration."
                    )

                value = parameters[parameter]

                if (
                    isinstance(value, bool)
                    or not isinstance(value, (int, float))
                    or not math.isfinite(value)
                    or value <= 0
                ):
                    raise ValueError(
                        f"Invalid value for {parameter} in {name}."
                    )

        return config

    # --------------------------------------------------
    # DASHBOARD INTERFACE
    # --------------------------------------------------

    def build_interface(self):

        container = ttk.Frame(
            self.root,
            padding=15
        )

        container.pack(
            fill="both",
            expand=True
        )

        # Header
        ttk.Label(
            container,
            text="REXPILOT",
            font=("Arial", 24, "bold")
        ).pack(anchor="w")

        ttk.Label(
            container,
            text="Chrome Dino Automation & Performance Lab",
            font=("Arial", 10)
        ).pack(
            anchor="w",
            pady=(0, 15)
        )

        # ----------------------------------------------
        # Strategy configuration
        # ----------------------------------------------

        settings = ttk.LabelFrame(
            container,
            text="Strategy Configuration",
            padding=12
        )

        settings.pack(
            fill="x",
            pady=5
        )

        self.strategy_var = tk.StringVar(
            value=self.config["selected_strategy"]
        )

        ttk.Label(
            settings,
            text="Playing Strategy:"
        ).grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.strategy_box = ttk.Combobox(
            settings,
            textvariable=self.strategy_var,
            values=list(self.STRATEGIES.keys()),
            state="readonly",
            width=25
        )

        self.strategy_box.grid(
            row=0,
            column=1,
            sticky="w",
            pady=5
        )

        self.strategy_box.bind(
            "<<ComboboxSelected>>",
            self.change_strategy
        )

        # Strategy parameters
        for index, parameter in enumerate(self.PARAMETERS):

            ttk.Label(
                settings,
                text=parameter.replace("_", " ").title()
            ).grid(
                row=index + 1,
                column=0,
                sticky="w",
                pady=4
            )

            value = self.config["strategies"][
                self.strategy_var.get()
            ][parameter]

            variable = tk.StringVar(
                value=str(value)
            )

            self.parameter_vars[parameter] = variable

            ttk.Entry(
                settings,
                textvariable=variable,
                width=25
            ).grid(
                row=index + 1,
                column=1,
                sticky="w",
                pady=4
            )

        # ----------------------------------------------
        # Session controls
        # ----------------------------------------------

        controls = ttk.LabelFrame(
            container,
            text="Session Controls",
            padding=12
        )

        controls.pack(
            fill="x",
            pady=10
        )

        self.start_button = ttk.Button(
            controls,
            text="Start Session",
            command=self.start_session
        )

        self.start_button.pack(
            side="left",
            padx=5
        )

        self.pause_button = ttk.Button(
            controls,
            text="Pause",
            command=self.toggle_pause,
            state="disabled"
        )

        self.pause_button.pack(
            side="left",
            padx=5
        )

        self.stop_button = ttk.Button(
            controls,
            text="Stop Session",
            command=self.stop_session,
            state="disabled"
        )

        self.stop_button.pack(
            side="left",
            padx=5
        )

        # ----------------------------------------------
        # Current session display
        # ----------------------------------------------

        status_frame = ttk.LabelFrame(
            container,
            text="Current Session",
            padding=12
        )

        status_frame.pack(
            fill="x",
            pady=5
        )

        self.timer_label = ttk.Label(
            status_frame,
            text="00:00:00",
            font=("Arial", 24, "bold")
        )

        self.timer_label.pack()

        self.status_label = ttk.Label(
            status_frame,
            text="No active session"
        )

        self.status_label.pack(pady=5)

        # ----------------------------------------------
        # Session history
        # ----------------------------------------------

        history_frame = ttk.LabelFrame(
            container,
            text="Session History",
            padding=10
        )

        history_frame.pack(
            fill="both",
            expand=True,
            pady=10
        )

        columns = (
            "session_id",
            "strategy",
            "duration",
            "score",
            "date"
        )

        self.history_table = ttk.Treeview(
            history_frame,
            columns=columns,
            show="headings",
            height=10
        )

        headings = {
            "session_id": "Session ID",
            "strategy": "Strategy",
            "duration": "Duration (s)",
            "score": "Final Score",
            "date": "Date"
        }

        widths = {
            "session_id": 120,
            "strategy": 120,
            "duration": 110,
            "score": 110,
            "date": 180
        }

        for column, heading in headings.items():

            self.history_table.heading(
                column,
                text=heading
            )

            self.history_table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            history_frame,
            orient="vertical",
            command=self.history_table.yview
        )

        self.history_table.configure(
            yscrollcommand=scrollbar.set
        )

        self.history_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        # ----------------------------------------------
        # Performance summary
        # ----------------------------------------------

        self.summary_label = ttk.Label(
            container,
            text="No recorded sessions yet.",
            font=("Arial", 10, "bold")
        )

        self.summary_label.pack(
            anchor="w",
            pady=5
        )

    # --------------------------------------------------
    # STRATEGY SELECTION
    # --------------------------------------------------

    def change_strategy(self, event=None):

        strategy_name = self.strategy_var.get()

        parameters = self.config["strategies"][strategy_name]

        for parameter in self.PARAMETERS:

            self.parameter_vars[parameter].set(
                str(parameters[parameter])
            )

    def create_strategy(self):

        strategy_name = self.strategy_var.get()

        strategy_class = self.STRATEGIES[strategy_name]

        strategy = strategy_class()

        parameters = {}

        # Validate dashboard parameter inputs
        for name in self.PARAMETERS:

            raw_value = self.parameter_vars[name].get().strip()

            try:
                value = float(raw_value)

            except ValueError as error:

                raise ValueError(
                    f"{name} must contain a numeric value."
                ) from error

            if not math.isfinite(value) or value <= 0:

                raise ValueError(
                    f"{name} must be a positive, finite number."
                )

            if value.is_integer():
                value = int(value)

            parameters[name] = value

            strategy.set_parameter(
                name,
                value
            )

        # Persist selected strategy and parameters
        updated_config = self.config.copy()

        updated_config["selected_strategy"] = strategy_name

        updated_config["strategies"] = (
            self.config["strategies"].copy()
        )

        updated_config["strategies"][strategy_name] = parameters

        with open(
            self.config_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                updated_config,
                file,
                indent=4
            )

        self.config = updated_config

        return strategy

    # --------------------------------------------------
    # START GAMEPLAY SESSION
    # --------------------------------------------------

    def start_session(self):

        if (
            self.current_session is not None
            and self.current_session.status in ("running", "paused")
        ):
            return

        try:

            # Load selected strategy and parameters
            strategy = self.create_strategy()

            # Launch Chrome
            self.controller.launch_browser()

            # Open Chrome Dino
            self.controller.open_game()

            # Start the dinosaur game
            self.controller.press_key(Keys.SPACE)

            # Create session record
            self.current_session = self.manager.start_session(
                strategy
            )

        except (
            ValueError,
            RuntimeError,
            WebDriverException,
            OSError
        ) as error:

            self.controller.close_browser()

            messagebox.showerror(
                "Session Error",
                str(error),
                parent=self.root
            )

            return

        self.last_duration = 0.0
        self.next_action = "jump"

        self.status_label.config(
            text=f"{strategy.name} session running"
        )

        self.start_button.config(
            state="disabled"
        )

        self.pause_button.config(
            state="normal",
            text="Pause"
        )

        self.stop_button.config(
            state="normal"
        )

        # Allow Chrome a brief moment before scheduling actions
        self.schedule_next_action(250)

        print(
            f"RexPilot session started using {strategy.name} strategy."
        )

    # --------------------------------------------------
    # GAMEPLAY ACTION SCHEDULER
    # --------------------------------------------------

    def schedule_next_action(self, delay_ms):

        if self.current_session is None:
            return

        if self.current_session.status != "running":
            return

        self.cancel_scheduled_action()

        self.action_job = self.root.after(
            max(0, int(delay_ms)),
            self.perform_next_action
        )

    def perform_next_action(self):

        self.action_job = None

        if self.current_session is None:
            return

        if self.current_session.status != "running":
            return

        try:

            parameters = (
                self.current_session.strategy.get_parameters()
            )

            if self.next_action == "jump":

                self.controller.jump(
                    parameters["jump_duration"]
                )

                print("Automated jump executed.")

                self.next_action = "duck"

                delay = parameters["delay_between_actions"]

            else:

                self.controller.duck(
                    parameters["duck_duration"]
                )

                print("Automated duck executed.")

                self.next_action = "jump"

                delay = parameters["waiting_interval"]

            self.schedule_next_action(
                delay * 1000
            )

        except Exception as error:

            self.handle_automation_error(error)

    def cancel_scheduled_action(self):

        if self.action_job is not None:

            try:

                self.root.after_cancel(
                    self.action_job
                )

            except tk.TclError:
                pass

            self.action_job = None

    # --------------------------------------------------
    # PAUSE AND RESUME
    # --------------------------------------------------

    def toggle_pause(self):

        if self.current_session is None:
            return

        try:

            if self.current_session.status == "running":

                # Cancel future gameplay actions
                self.cancel_scheduled_action()

                # Pause session timing
                self.manager.pause_session()

                self.pause_button.config(
                    text="Resume"
                )

                self.status_label.config(
                    text="Session paused"
                )

                print("RexPilot automation paused.")

            elif self.current_session.status == "paused":

                # Resume session timing
                self.manager.resume_session()

                self.pause_button.config(
                    text="Pause"
                )

                self.status_label.config(
                    text="Session resumed"
                )

                print("RexPilot automation resumed.")

                # Resume scheduled actions
                self.schedule_next_action(0)

        except RuntimeError as error:

            messagebox.showerror(
                "Session Error",
                str(error),
                parent=self.root
            )

    # --------------------------------------------------
    # STOP SESSION AND COLLECT SCORE
    # --------------------------------------------------

    def stop_session(self):

        if self.current_session is None:
            return

        # Cancel scheduled gameplay actions
        self.cancel_scheduled_action()

        try:

            # Record session completion time
            completed_session = self.manager.stop_session()

        except RuntimeError as error:

            messagebox.showerror(
                "Session Error",
                str(error),
                parent=self.root
            )

            return

        self.last_duration = completed_session.get_duration()

        # Collect score manually
        final_score = simpledialog.askinteger(
            "Final Score",
            "Enter the final Chrome Dino score.\n"
            "Select Cancel to skip score entry.",
            minvalue=0,
            parent=self.root
        )

        try:

            completed_session.set_final_score(
                final_score
            )

            # Save completed session
            record = self.logger.log_session(
                completed_session
            )

            # Update dashboard history
            self.add_history_record(record)

            print("Session recorded successfully.")

        except (
            RuntimeError,
            OSError,
            ValueError,
            TypeError
        ) as error:

            messagebox.showerror(
                "Logging Error",
                str(error),
                parent=self.root
            )

        finally:

            # Close Chrome
            self.controller.close_browser()

            # Reset session state
            self.current_session = None

            self.reset_session_controls()

            self.status_label.config(
                text="Session completed"
            )

    def reset_session_controls(self):

        self.start_button.config(
            state="normal"
        )

        self.pause_button.config(
            state="disabled",
            text="Pause"
        )

        self.stop_button.config(
            state="disabled"
        )

    # --------------------------------------------------
    # AUTOMATION ERROR HANDLING
    # --------------------------------------------------

    def handle_automation_error(self, error):

        print(
            f"Automation error: {error}"
        )

        self.cancel_scheduled_action()

        try:

            # Finish and record the interrupted session
            if (
                self.current_session is not None
                and self.current_session.status in (
                    "running",
                    "paused"
                )
            ):

                completed_session = self.manager.stop_session()

                self.last_duration = (
                    completed_session.get_duration()
                )

                # Score remains blank because gameplay was interrupted
                record = self.logger.log_session(
                    completed_session
                )

                self.add_history_record(record)

        except Exception as logging_error:

            messagebox.showerror(
                "Logging Error",
                str(logging_error),
                parent=self.root
            )

        finally:

            # Ensure browser cleanup
            self.controller.close_browser()

            self.current_session = None

            self.reset_session_controls()

            self.status_label.config(
                text="Automation stopped due to an error"
            )

            messagebox.showerror(
                "Automation Error",
                str(error),
                parent=self.root
            )

    # --------------------------------------------------
    # SESSION TIMER
    # --------------------------------------------------

    def update_timer(self):

        if self.current_session is not None:

            duration = self.current_session.get_duration()

            # Check configured session duration
            if self.current_session.status == "running":

                session_limit = (
                    self.current_session.strategy
                    .get_parameters()["session_duration"]
                )

                if duration >= session_limit:

                    print(
                        "Configured session duration reached."
                    )

                    self.stop_session()

                    duration = self.last_duration

        else:

            duration = self.last_duration

        seconds = int(duration)

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        remaining = seconds % 60

        self.timer_label.config(
            text=f"{hours:02}:{minutes:02}:{remaining:02}"
        )

        self.root.after(
            250,
            self.update_timer
        )

    # --------------------------------------------------
    # SESSION HISTORY
    # --------------------------------------------------

    def load_history(self):

        if not self.logger.file_path.exists():
            return

        try:

            with open(
                self.logger.file_path,
                "r",
                newline="",
                encoding="utf-8"
            ) as file:

                reader = csv.DictReader(file)

                for record in reader:

                    self.add_history_record(
                        record
                    )

        except (OSError, csv.Error) as error:

            messagebox.showerror(
                "History Loading Error",
                str(error),
                parent=self.root
            )

    def add_history_record(self, record):

        session_id = str(
            record.get("session_id", "")
        )

        strategy = record.get("strategy", "")

        duration = record.get(
            "session_duration",
            ""
        )

        score = record.get(
            "final_score",
            ""
        )

        date = str(
            record.get("date", "")
        )

        if score is None or score == "":
            displayed_score = "Not entered"
        else:
            displayed_score = score

        # Add session to history table
        self.history_table.insert(
            "",
            "end",
            values=(
                session_id[:8],
                strategy,
                duration,
                displayed_score,
                date[:19]
            )
        )

        self.history_count += 1

        # Track valid scores for summary
        try:

            if score is not None and score != "":

                numeric_score = float(score)

                if math.isfinite(numeric_score):
                    self.history_scores.append(numeric_score)

        except (ValueError, TypeError):
            pass

        self.update_summary()

    # --------------------------------------------------
    # PERFORMANCE SUMMARY
    # --------------------------------------------------

    def update_summary(self):

        if not self.history_scores:

            self.summary_label.config(
                text=(
                    f"Recorded sessions: {self.history_count} | "
                    "No scored sessions available."
                )
            )

            return

        average = (
            sum(self.history_scores)
            / len(self.history_scores)
        )

        highest = max(
            self.history_scores
        )

        self.summary_label.config(
            text=(
                f"Recorded sessions: {self.history_count} | "
                f"Average score: {average:.2f} | "
                f"Highest score: {highest:g}"
            )
        )

    # --------------------------------------------------
    # DASHBOARD SHUTDOWN
    # --------------------------------------------------

    def close_dashboard(self):

        if (
            self.current_session is not None
            and self.current_session.status in (
                "running",
                "paused"
            )
        ):

            confirm = messagebox.askyesno(
                "Active Session",
                "A gameplay session is still active.\n\n"
                "Stop the session and close RexPilot?",
                parent=self.root
            )

            if not confirm:
                return

            self.stop_session()

            # If stopping failed, keep dashboard open
            if self.current_session is not None:
                return

        # Cancel any remaining scheduled callbacks
        self.cancel_scheduled_action()

        # Ensure Chrome is closed
        self.controller.close_browser()

        self.root.destroy()

    # --------------------------------------------------
    # APPLICATION ENTRY
    # --------------------------------------------------

    def run(self):

        self.root.mainloop()


if __name__ == "__main__":

    try:

        dashboard = RexPilotDashboard()

        dashboard.run()

    except (FileNotFoundError, ValueError, OSError) as error:

        print(f"RexPilot startup error: {error}")

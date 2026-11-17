import uuid
from datetime import datetime


class GameSession:

    def __init__(self):
        self.strategy = None
        self.start_time = None
        self.end_time = None
        self.final_score = None
        self.status = "not_started"
        self.session_id = str(uuid.uuid4())

        self.paused_at = None
        self.total_paused_time = 0.0

    def start(self, strategy):
        if self.status != "not_started":
            raise RuntimeError("Session has already been started.")

        self.strategy = strategy
        self.start_time = datetime.now()
        self.status = "running"

        print(f"Session started using {strategy.name} strategy.")

    def pause(self):
        if self.status != "running":
            raise RuntimeError("Only running sessions can be paused.")

        self.paused_at = datetime.now()
        self.status = "paused"

    def resume(self):
        if self.status != "paused":
            raise RuntimeError("Only paused sessions can be resumed.")

        self.total_paused_time += (
            datetime.now() - self.paused_at
        ).total_seconds()

        self.paused_at = None
        self.status = "running"

    def finish(self, final_score=None):
        if self.status not in ("running", "paused"):
            raise RuntimeError("No active session to finish.")

        current_time = datetime.now()

        if self.paused_at is not None:
            self.total_paused_time += (
                current_time - self.paused_at
            ).total_seconds()

            self.paused_at = None

        self.end_time = current_time
        self.final_score = final_score
        self.status = "completed"

        print("Session completed.")

    def get_duration(self):
        if self.start_time is None:
            return 0

        end_time = self.end_time or datetime.now()

        paused_time = self.total_paused_time

        if self.paused_at is not None:
            paused_time += (
                end_time - self.paused_at
            ).total_seconds()

        return max(
            0,
            (end_time - self.start_time).total_seconds() - paused_time
        )
    def set_final_score(self, final_score):

        if self.status != "completed":
            raise RuntimeError(
                "Final score can only be recorded after session completion."
            )

        if final_score is not None:

            if isinstance(final_score, bool) or not isinstance(final_score, int):
                raise TypeError("Final score must be a whole number.")

            if final_score < 0:
                raise ValueError("Final score cannot be negative.")

        self.final_score = final_score
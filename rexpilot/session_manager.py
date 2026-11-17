from rexpilot.game_session import GameSession


class SessionManager:

    def __init__(self):
        self.current_session = None
        self.sessions = []
        self.is_paused = False

    def start_session(self, strategy):

        if (
            self.current_session is not None
            and self.current_session.status in ("running", "paused")
        ):
            raise RuntimeError("Another session is already active.")

        session = GameSession()
        session.start(strategy)

        self.current_session = session
        self.sessions.append(session)
        self.is_paused = False

        return session

    def pause_session(self):

        if self.current_session is None:
            raise RuntimeError("No session is available.")

        self.current_session.pause()
        self.is_paused = True

        print("Session paused.")

    def resume_session(self):

        if self.current_session is None:
            raise RuntimeError("No session is available.")

        self.current_session.resume()
        self.is_paused = False

        print("Session resumed.")

    def stop_session(self, final_score=None):

        if self.current_session is None:
            raise RuntimeError("No session is available.")

        self.current_session.finish(final_score)

        self.is_paused = False

        print("Session stopped.")

        return self.current_session

    def restart_session(self):

        if self.current_session is None:
            raise RuntimeError("No session is available to restart.")

        strategy = self.current_session.strategy

        if self.current_session.status in ("running", "paused"):
            self.current_session.finish()

        print("Restarting session...")

        return self.start_session(strategy)
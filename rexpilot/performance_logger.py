import csv
from pathlib import Path
from datetime import datetime


class PerformanceLogger:

    FIELDNAMES = [
        "session_id",
        "strategy",
        "jump_duration",
        "duck_duration",
        "session_duration",
        "final_score",
        "date"
    ]

    def __init__(self, file_path=None):

        self.records = []

        if file_path is None:
            self.file_path = (
                Path(__file__).resolve().parent.parent / "sessions.csv"
            )
        else:
            self.file_path = Path(file_path)

    def log_session(self, session):

        if session.status != "completed":
            raise RuntimeError(
                "Only completed sessions can be logged."
            )

        if session.strategy is None:
            raise RuntimeError(
                "Session does not have an assigned strategy."
            )

        parameters = session.strategy.get_parameters()

        record = {
            "session_id": session.session_id,
            "strategy": session.strategy.name,
            "jump_duration": parameters["jump_duration"],
            "duck_duration": parameters["duck_duration"],
            "session_duration": round(session.get_duration(), 2),
            "final_score": (
                session.final_score
                if session.final_score is not None
                else ""
            ),
            "date": datetime.now().isoformat(timespec="seconds")
        }

        file_exists = self.file_path.exists()

        needs_header = (
            not file_exists or self.file_path.stat().st_size == 0
        )

        with open(
            self.file_path,
            mode="a",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=self.FIELDNAMES
            )

            if needs_header:
                writer.writeheader()

            writer.writerow(record)

        self.records.append(record)

        print("Session successfully recorded.")

        return record
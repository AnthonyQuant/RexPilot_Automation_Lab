from rexpilot.playing_strategy import PlayingStrategy


class AggressiveStrategy(PlayingStrategy):

    def __init__(self):
        parameters = {
            "jump_duration": 0.06,
            "duck_duration": 0.10,
            "delay_between_actions": 0.50,
            "waiting_interval": 1.00,
            "session_duration": 60
        }

        super().__init__(
            name="Aggressive",
            parameters=parameters
        )
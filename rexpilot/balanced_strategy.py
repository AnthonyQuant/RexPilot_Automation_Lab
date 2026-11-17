from rexpilot.playing_strategy import PlayingStrategy


class BalancedStrategy(PlayingStrategy):

    def __init__(self):
        parameters = {
            "jump_duration": 0.08,
            "duck_duration": 0.15,
            "delay_between_actions": 1.00,
            "waiting_interval": 1.50,
            "session_duration": 60
        }

        super().__init__(
            name="Balanced",
            parameters=parameters
        )
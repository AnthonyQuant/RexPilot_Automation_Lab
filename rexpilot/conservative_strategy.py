from rexpilot.playing_strategy import PlayingStrategy


class ConservativeStrategy(PlayingStrategy):

    def __init__(self):
        parameters = {
            "jump_duration": 0.10,
            "duck_duration": 0.20,
            "delay_between_actions": 1.50,
            "waiting_interval": 2.00,
            "session_duration": 60
        }

        super().__init__(
            name="Conservative",
            parameters=parameters
        )
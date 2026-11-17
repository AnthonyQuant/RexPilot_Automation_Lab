class PlayingStrategy:

    def __init__(self, name, parameters=None):
        self.name = name
        self.parameters = parameters or {}

    def get_parameters(self):
        return self.parameters.copy()

    def set_parameter(self, parameter, value):
        if parameter not in self.parameters:
            raise KeyError(f"Unknown parameter: {parameter}")

        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("Parameter value must be numeric.")

        if value <= 0:
            raise ValueError("Parameter value must be greater than zero.")

        self.parameters[parameter] = value
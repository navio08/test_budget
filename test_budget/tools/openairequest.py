import abc


class OpenAIRequest(abc.ABC):
    def __init__(self, api_key):
        self.api_key = api_key
        self.messages = [{"role": "user"}]
        self.response = None

    @abc.abstractmethod
    def __call__(self): ...

    @abc.abstractmethod
    def output(self, response, **kwargs): ...

    def is_valid_reasoning_effort(self, value: str) -> bool:
        return value in ["minimal", "low", "medium", "high"]
    
    def is_valid_temperature(self, value: str) -> bool:
        return (value >= 0) and (value <=2)
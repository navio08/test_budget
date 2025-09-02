import abc


class OpenAIRequest(abc.ABC):
    def __init__(self, api_key):
        self.api_key = api_key
        self.messages = [{"role": "user"}]

    @abc.abstractmethod
    def call(self): ...

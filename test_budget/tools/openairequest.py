import abc


class OpenAIRequest(abc.ABC):
    def __init__(self, api_key):
        self.api_key = api_key
        self.messages = [{"role": "user"}]
        self.response = None

    @abc.abstractmethod
    def call(self): ...

    @abc.abstractmethod
    def output(self, response, **kwargs): ...
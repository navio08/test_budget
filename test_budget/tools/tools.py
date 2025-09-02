
from tools.openairequest import OpenAIRequest
from tools.chat_completion import ChatCompletion
from tools.response import ResponseOpenAI
from tools.mock import MockOpenAI


def create_openai_request(api_key, tool) -> OpenAIRequest:
    return {
        "chat_completion": ChatCompletion(api_key),
        "response": ResponseOpenAI(api_key),
        "mock": MockOpenAI(api_key)
    }[tool]

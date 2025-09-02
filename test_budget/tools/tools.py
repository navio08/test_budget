
from tools.openairequest import OpenAIRequest
from tools.chat_completion import ChatCompletion
from tools.response import ResponseOpenAI
from tools.mock import MockOpenAI


def create_openai_request(tool, api_key=None) -> OpenAIRequest:
    if not api_key:
        return MockOpenAI(api_key)

    return {
        "chat_completion": ChatCompletion(api_key),
        "response": ResponseOpenAI(api_key),
    }[tool]

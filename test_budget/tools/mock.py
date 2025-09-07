import pprint
import ast
from tools.openairequest import OpenAIRequest


class MockOpenAI(OpenAIRequest):
    def call(self, prompt: str, model: str):
        return str({
            "WEDDING_SUBCATEGORY_WEDDING_VENUES": 2000,
            "WEDDING_SUBCATEGORY_CATERING": 15300,
            "WEDDING_SUBCATEGORY_LAWYER": 150,
            "WEDDING_SUBCATEGORY_PHOTOGRAPHER": 1700,
            "WEDDING_SUBCATEGORY_VIDEOGRAPHER": 1300,
            "WEDDING_SUBCATEGORY_DEEJAY": 1050,
            "WEDDING_SUBCATEGORY_FLOWERS": 800,
            "WEDDING_SUBCATEGORY_BRIDE_DRESS": 1000,
            "WEDDING_SUBCATEGORY_GROOM_SUITS": 400,
            "WEDDING_SUBCATEGORY_GUEST_INVITATIONS": 200,
            "WEDDING_SUBCATEGORY_MAKEUP_BRIDE": 250,
            "WEDDING_SUBCATEGORY_HAIR_SALON_BRIDE": 250,
            "WEDDING_SUBCATEGORY_BAKERY": 300,
            "WEDDING_SUBCATEGORY_WEDDING_DECORATION": 300
        })

    def output(self, response, **kwargs):
        result = ["=" * 50]
        # Handle OpenAI SDK response object
        result.append(pprint.pformat(ast.literal_eval(response), width=80, depth=None))
        if kwargs:
            result.extend(("=" * 50, "kwargs:"))
            [result.append(f"\t{k}:{v}") for k, v in kwargs.items()]
        return "\n".join(result)
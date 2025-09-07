import pprint
from openai import OpenAI
import json
from tools.openairequest import OpenAIRequest


class ResponseOpenAI(OpenAIRequest):
    def __call__(self, prompt, model="gpt-3.5-turbo"):
        return OpenAI(api_key=self.api_key).responses.create(
            background=False,
            include=None,
            input=prompt,
            instructions="Return ONLY a valid JSON object with allocated amounts.",  # <-- Dina
            max_output_tokens=10000,
            max_tool_calls=1,
            metadata=None,
            model=model,
            parallel_tool_calls=False,
            prompt=None,
            prompt_cache_key=None,
            reasoning={"effort": "low"},
            store=False,
            stream=False,
            stream_options=None,
            text={"format": {"type": "json_schema", "name": "wedding_budget",
                "schema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": {"type": "number"}
                },
            }},
            tool_choice=None,
            tools=[{"type": "web_search"}],
            top_logprobs=None,
            top_p=1,
            truncation="auto",
            user=None,

            # doesnt work with gpt-5
            # temperature=0.2,
        )

    def output(self, response, **kwargs):
        result = ["=" * 50]
        message = response.output_text

        result.append(pprint.pformat(json.loads(message), width=80, depth=None))
        result.extend(
            (
                "=" * 50,
                "\nTokens utilizados:",
                f"  Prompt:\t{response.usage.input_tokens}\tPrompt Cached:\t{response.usage.input_tokens_details.cached_tokens}",
                f"  Completion:\t{response.usage.output_tokens}\tReasoning:\t{response.usage.output_tokens_details.reasoning_tokens}\tOutput:\t{response.usage.output_tokens-response.usage.output_tokens_details.reasoning_tokens}",
                f"  Total:\t{response.usage.total_tokens}",
            )
        )
        if kwargs:
            result.extend(("=" * 50, "kwargs:"))
            [result.append(f"\t{k}:{v}") for k, v in kwargs.items()]
        return "\n".join(result)
import json
import pprint
from openai import OpenAI

from tools.openairequest import OpenAIRequest


class ChatCompletion(OpenAIRequest):
    def __call__(self, prompt, model="gpt-3.5-turbo", ):
        return OpenAI(api_key=self.api_key).chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            reasoning_effort="low",
            top_p=1,  # dont use with temperature
            frequency_penalty=0,
            presence_penalty=0,
            logit_bias=None,
            response_format={"type": "json_schema", "json_schema": {
                "name": "wedding_budget",
                "strict": False,
                "schema": {
                    "type": "object",
                    "properties": {},
                    "additionalProperties": {"type": "number"}
                },
            }},
            stream=False,
            verbosity="low",

            # doesnt work with gpt-5
            # max_tokens=10000, # doesnt work with gpt-5
            # temperature=0.5, # doesnt work with gpt-5
            # logprobs=None, # doesnt work with gpt-5
            # modalities=["text"], # doesnt work with gpt-5
            # web_search_options={
            #     "user_location": "Madrid, Spain",
            #     "search_context_size": "high",
            #     "search_depth": "deep",
            #     "search_type": "web",
            #     "search_count": 1,
            #     "search_offset": 0,
            #     "search_exclude_domains": [],
            #     "search_include_domains": [],
            #     "search_exclude_urls": [],
            # },  # doesnt work with gpt-5
        )

    def output(self, response, **kwargs):
        result = ["=" * 50]
        # Handle OpenAI SDK response object
        if hasattr(response, 'choices') and len(response.choices) > 0:
            message = response.choices[0].message.content
            result.append(pprint.pformat(json.loads(message), width=80, depth=None))
        else:
            result.extend(("Respuesta inesperada:", str(response)))
        if hasattr(response, 'usage') and response.usage:
            result.extend(
                (
                    "=" * 50,
                    "\nTokens utilizados:",
                    f"  Prompt:\t{response.usage.prompt_tokens}\tPrompt Cached:\t{response.usage.prompt_tokens_details.cached_tokens}",
                    f"  Completion:\t{response.usage.completion_tokens}\tReasoning:\t{response.usage.completion_tokens_details.reasoning_tokens}\tOutput:\t{response.usage.completion_tokens-response.usage.completion_tokens_details.reasoning_tokens}",
                    f"  Total:\t{response.usage.total_tokens}",
                )
            )
        if kwargs:
            result.extend(("=" * 50, "kwargs:"))
            [result.append(f"\t{k}:{v}") for k, v in kwargs.items()]
        return "\n".join(result)
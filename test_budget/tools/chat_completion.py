
from openai import OpenAI

from tools.openairequest import OpenAIRequest


class ChatCompletion(OpenAIRequest):
    def call(self, prompt, model="gpt-3.5-turbo", ):
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
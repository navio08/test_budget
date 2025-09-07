import pprint
from openai import OpenAI
import json
from tools.openairequest import OpenAIRequest


class ResponseOpenAI(OpenAIRequest):
    def __call__(self, prompt: str, model="gpt-3.5-turbo", developer_prompt: str = "", reasoning_effort: str = "low", temperature: int = 1):
        # verify valid inputs
        if not self.is_valid_reasoning_effort(reasoning_effort):
            raise ValueError(f"Invalid reasoning_effort value. Given: {reasoning_effort}. Accepted: minimal, low, medium, and high.")
        
        if not self.is_valid_temperature(temperature):
            raise ValueError(f"Invalid temperature value. Given {temperature}. Accepted 0 <= temperature <= 2.")
        
        return OpenAI(api_key=self.api_key).responses.create(
            background=False, # False means model response will not run in the background
            ### Parameters that control LLM inference itself
            model=model,
            input=[
                # developer role
                {
                    "role": "developer",
                    "content": developer_prompt,
                },
                # user role
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            # instructions="Return ONLY a valid JSON object with allocated amounts.",  # using instructions is equivalent to using roles in the input # High level instructions on behaviour: tone, goals, examples. Instructions here take priority over the input
            reasoning={
                "effort": reasoning_effort, # options: minimal, low, medium, and high
                "summary": None,
            },
            temperature=temperature, # <-- Dina.  value between 0-2. Lower values (towards 0)--> More deterministic output, Higher values: more "creative" output
            top_p=1, # recommendations: modify either temperature or top_p, but not both            
            ### Parameters that control how the model does the inference
            max_tool_calls=1,
            parallel_tool_calls=False,
            prompt=None, # only useful if we use the prompt library ()
            prompt_cache_key=None,     
            tool_choice=None, # versatile parameter to call different types of tools to generate response
            tools=[{"type": "web_search"}], # default tools supported by OpenAI API: https://platform.openai.com/docs/guides/tools
            top_logprobs=None,
            ### Response configuration
            text = { # <-- Dina. Define a class with predefined wedding categories and use it with structured outputs
                "format": {
                    "type": "json_schema",
                    "name": "wedding_budget",
                    "schema": {
                        "type": "object",
                        "properties": {},
                        "additionalProperties": {"type": "number"}
                    },
                }
            },
            include=None,
            max_output_tokens=10000, # includes visible output tokens and reasoning tokens            
            metadata=None,                   
            store=False,
            stream=False,
            stream_options=None,
            truncation="auto",
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
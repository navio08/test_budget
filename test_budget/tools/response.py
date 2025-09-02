from tools.openairequest import OpenAIRequest


class ResponseOpenAI(OpenAIRequest):
    def call(self, prompt, model="gpt-3.5-turbo"):
        return self.model.responses.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
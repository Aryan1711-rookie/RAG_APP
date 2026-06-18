from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()


class LLMResponse:
    """
    Wrapper to mimic LangChain response.content
    """

    def __init__(self, content: str):
        self.content = content


class GroqClient:

    def __init__(
        self,
        model_name: str = "llama-3.3-70b-versatile"
    ):

        self.api_key = os.getenv(
            "GROQ_API_KEY"
        )

        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY not found"
            )

        self.model_name = model_name

        self.client = Groq(
            api_key=self.api_key
        )

        print(
            f"Groq model loaded: "
            f"{self.model_name}"
        )

    def invoke(
        self,
        prompt: str
    ) -> LLMResponse:

        response = (
            self.client.chat.completions.create(
                model=self.model_name,

                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],

                temperature=0.2
            )
        )

        answer = (
            response
            .choices[0]
            .message
            .content
        )

        return LLMResponse(
            content=answer
        )
    def stream(self, prompt):
        stream = (self.client.chat.completions.create(model=self.model_name,
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ],
            stream=True
            )
        )

        for chunk in stream:

            token = (
            chunk.choices[0]
            .delta
            .content
            )

        if token:
            yield token
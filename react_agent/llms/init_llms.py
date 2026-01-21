from .base import LLM
from openai import AsyncOpenAI
from google import genai

class OpenAILLM(LLM):
    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def generate(self, messages: list[dict]) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
        )

        return response.choices[0].message.content




class GeminiLLM(LLM):
    def __init__(
        self,
        api_key: str,
        model: str,
        temperature: float = 0.0,
        max_tokens: int = 512,
    ):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.temperature = temperature

    async def generate(self, messages: list[dict]) -> str:
        prompt = self._convert_messages_to_prompt(messages)

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config={
                "temperature": self.temperature,
            },
        )

        return response.text.strip()

    def _convert_messages_to_prompt(self, messages):
        parts = []
        for msg in messages:
            role = msg["role"].upper()
            content = msg["content"]
            parts.append(f"[{role}]\n{content}")
        return "\n\n".join(parts)

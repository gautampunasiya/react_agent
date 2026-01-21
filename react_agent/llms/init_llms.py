from .base import LLM
from openai import AsyncOpenAI
import google.generativeai as genai


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
        genai.configure(api_key=api_key)

        self.model_name = model
        self.temperature = temperature
        self.model = genai.GenerativeModel(model)

    async def generate(self, messages: list[dict]) -> str:
        prompt = self._convert_messages_to_prompt(messages)
        response = self.model.generate_content(
            prompt,
            generation_config={
                "temperature": self.temperature,
            },
        )

        return response.text.strip()

    def _convert_messages_to_prompt(self, messages):
        prompt_parts = []

        for msg in messages:
            role = msg["role"]
            content = msg["content"]

            if role == "system":
                prompt_parts.append(f"[SYSTEM]\n{content}")
            elif role == "user":
                prompt_parts.append(f"[USER]\n{content}")
            elif role == "assistant":
                prompt_parts.append(f"[ASSISTANT]\n{content}")

        return "\n\n".join(prompt_parts)

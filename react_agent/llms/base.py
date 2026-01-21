from abc import ABC, abstractmethod

class LLM(ABC):
    @abstractmethod
    async def generate(self, messages: list[dict]) -> str:
        """
        messages: [{"role": "system" | "user" | "assistant", "content": str}]
        returns: raw text from the model
        """
        pass
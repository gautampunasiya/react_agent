from abc import ABC, abstractmethod
import asyncio
from pydantic import BaseModel


class Tool(ABC):
    name: str
    description: str
    input_schema: BaseModel
    timeout: int = 10
    retries: int = 1

    @abstractmethod
    async def _run(self, input: BaseModel):
        pass

    async def run(self, input_dict: dict):
        data = self.input_schema(**input_dict)
        last_error = None

        for _ in range(self.retries):
            try:
                return await asyncio.wait_for(
                    self._run(data),
                    timeout=self.timeout
                )
            except Exception as e:
                last_error = e

        raise last_error

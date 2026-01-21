"""Basic example of using React Agent."""
import asyncio
from react_agent.llms.openai_llm import OpenAILLM
from react_agent.core.react_agent import ReactAgent
from react_agent.tools.calculator import CalculatorTool
from react_agent.core.memory import Memory

llm = OpenAILLM(
    api_key="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",
    model="gpt-5.1"
)

async def main():
    agent = ReactAgent(
        llm=llm,
        tools=[CalculatorTool()],
        memory=Memory(),
        verbose=True
    )

    result = await agent.run("what is 12 divided by 4 plus 3?")
asyncio.run(main())
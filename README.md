# React Agent

A Python framework for building agent systems with reasoning (ReAct pattern).

## Features

- ReAct (Reasoning + Acting) agent framework
- Tool registry and management
- Multiple LLM support (OpenAI, Gemeni)
- Memory management
- Verbose logging and debugging

## Installation


```bash
pip install git+https://github.com/gautampunasiya/react_agent.git
```

## Quick Start

```python
import asyncio
from react_agent.llms.init_llms import OpenAILLM, GeminiLLM
from react_agent.core.react_agent import ReactAgent
from react_agent.tools.calculator import CalculatorTool
from react_agent.tools.web_search import SearchTool
from react_agent.core.memory import Memory
import os
from dotenv import load_dotenv
load_dotenv()

import nest_asyncio
nest_asyncio.apply()

llm=GeminiLLM(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model=os.getenv("GOOGLE_GEMINI_MODEL"),
        )

async def main():
    agent = ReactAgent(
        llm=llm,
        tools=[CalculatorTool(), SearchTool('Tavily_API_Key')],
        memory=Memory(),
        verbose=True
    )

    result = await agent.run("what is 37 multiplied by 24?")
asyncio.run(main())
# Use the agent...
```

## Documentation

For more information, see the [documentation](docs/) and [examples](examples/).

## License

MIT License - see LICENSE file for details

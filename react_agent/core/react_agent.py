from react_agent.tools.registry import ToolRegistry
from react_agent.core.prompt import build_react_prompt
from react_agent.core.parser import parse_react_output
from react_agent.core.verbose import VerboseLogger

class Agent:
    def __init__(self, llm, tools=None, memory=None):
        self.llm = llm
        self.tools = ToolRegistry(tools)
        self.memory = memory

class ReactAgent(Agent):
    def __init__(self, llm, tools=None, memory=None, max_steps=10,verbose=False):
        super().__init__(llm, tools, memory)
        self.max_steps = max_steps
        self.verbose_logger = VerboseLogger(verbose)

    async def run(self, user_input: str):
        self.verbose_logger.log("> Entering new AgentExecutor chain...\n") 

        agent_scratchpad = ""

        for step in range(self.max_steps):
            
            prompt = build_react_prompt(
                tools=self.tools.describe_for_prompt(),
                tool_names=", ".join(self.tools._tools.keys())if self.tools._tools else "none",
                user_input=user_input,
                agent_scratchpad=agent_scratchpad
                )
            self.memory.add("system", prompt)
            response = await self.llm.generate([{"role": "user", "content": prompt}])

            self.memory.add("assistant", response)
            self.verbose_logger.log(response.strip())
            parsed = parse_react_output(response)

            if parsed["type"] in ("final", "direct"):
                self.verbose_logger.log("\n> Finished chain.")
                return parsed["output"]          


            tool = self.tools.get(parsed["tool"])
            if not tool:
                raise RuntimeError(
                    f"Tool '{parsed['tool']}' not found. "
                    f"Available tools: {list(self.tools._tools.keys())}"
                )
            
            self.verbose_logger.log(
                f"Action: {parsed['tool']}\n"
                f"Action Input: {parsed['input']}"
            )

            observation = await tool.run(parsed["input"])
            self.verbose_logger.log(f"Observation: {observation}\n")
            self.memory.add(
                "assistant",
                f"Observation: {observation}"
            )

        raise Exception("Max steps exceeded")

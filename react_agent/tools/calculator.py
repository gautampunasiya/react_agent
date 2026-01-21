from anthropic import BaseModel
from react_agent.tools.base import Tool



class CalculatorInput(BaseModel):
    expression: str


class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluate a math expression like 2 + 2"
    input_schema = CalculatorInput

    async def _run(self, input: CalculatorInput):
        return eval(input.expression)
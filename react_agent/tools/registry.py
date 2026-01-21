class ToolRegistry:
    def __init__(self, tools=None):
        self._tools = {}
        if tools:
            for tool in tools:
                self.register(tool)

    def register(self, tool):
        self._tools[tool.name] = tool

    def get(self, name: str):
        return self._tools.get(name)

    def list(self):
        return list(self._tools.values())

    def describe_for_prompt(self) -> str:
        """
        Used to inject tool info into the LLM prompt
        """
        lines = []
        for tool in self._tools.values():
            schema = tool.input_schema.model_json_schema()
            lines.append(
                f"- {tool.name}: {tool.description}\n"
                f"  input_schema: {schema}"
            )
        return "\n".join(lines)
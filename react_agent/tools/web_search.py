from anthropic import BaseModel
from react_agent.tools.base import Tool
from tavily import TavilyClient

class websearch(BaseModel):
    query: str

class SearchTool(Tool):
    name = "Web search"
    description = "Search the web for information"
    input_schema = websearch

    def __init__(self, api_key: str):
        super().__init__()
        self.api_key = api_key

    async def _run(self, input: websearch):
        client = TavilyClient(api_key=self.api_key)
        response = client.search(
            query=input.query,
            search_depth="advanced"
        )
        return response['results'][0]['content']
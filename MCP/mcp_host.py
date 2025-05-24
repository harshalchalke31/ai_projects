from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import arxiv_tool, save_tool, search_tool, wiki_tool
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
class ResponseTemplate(BaseModel):
    topic: str
    answer: str
    summary: str
    sources: list[str]
    tools: list[str]

class MCPHost:
    def __init__(self):
        llm = ChatGroq(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            api_key=os.environ["GROQ_API_KEY"]
        )

        self.tools = [arxiv_tool, save_tool, search_tool, wiki_tool]
        self.parser = PydanticOutputParser(pydantic_object=ResponseTemplate)

        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are an advanced research assistant.
        Your task is to answer complex queries using external tools when necessary.

        You can call tools like WikipediaSearch, DuckDuckGoSearch, ArxivSearch, and SaveToDocx
        to gather information. After gathering all the required data and reasoning through it,
        you MUST return a structured JSON with the following fields:

        - topic: the main subject of the query
        - answer: a full explanation using facts and reasoning
        - summary: a brief version of the answer
        - sources: list of references or keywords from tools
        - tools: list of tool names you used

        Only return JSON in the final output step, following this format:

        {format_instructions}
        """
            ),
            ("placeholder", "{chat_history}"),
            ("human", "{query}"),
            ("placeholder", "{agent_scratchpad}"),
        ]).partial(format_instructions=self.parser.get_format_instructions())


        agent = create_tool_calling_agent(llm=llm, prompt=self.prompt, tools=self.tools)
        self.agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

    def run_agent_query(self, query: str):
        try:
            response = self.agent_executor.invoke({"query": query})
            parsed = self.parser.parse(response["output"])
            return parsed
        except Exception as e:
            return {"error": str(e), "raw": str(response) if 'response' in locals() else "N/A"}

    def run_tool(self, tool_name, input_str):
        try:
            tool_map = {t.name: t.func for t in self.tools}
            if tool_name in tool_map:
                return tool_map[tool_name](input_str)
            return f"Tool '{tool_name}' not found."
        except Exception as e:
            return f"Error running tool '{tool_name}': {str(e)}"

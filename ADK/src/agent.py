import os
from dotenv import load_dotenv
import litellm
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from .tools.utils import *


load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY not initialized")

# litellm configuration
litellm.num_retries=0
litellm.telemetry=False
litellm.set_verbose=False




root_agent = Agent(
    name="dad_joke_agent",
    model=LiteLlm(model="groq/meta-llama/llama-4-scout-17b-16e-instruct",
                  api_key=os.getenv("GROQ_API_KEY"),
                  max_tokens=600,
                  temperature=0.2),
    description="tool_calling_agent",
    instruction="""
You are a tool-using assistant.

Available tools:
- get_current_time
- web_search

Rules:
1. Always check if a tool can help before answering.
   If a tool is relevant, you MUST use it.
2. Use tools as follows:
   - get_current_time → when date or time is asked or implied
   - web_search → for factual, recent, or external information
3. Call tools first.
4. Do NOT answer from memory if a tool applies.
    """,
    tools=[get_current_time,web_search,write_email],
)



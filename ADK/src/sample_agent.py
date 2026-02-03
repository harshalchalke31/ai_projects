import os
import asyncio
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("GROQ_API_KEY not set")

agent = Agent(
    name="groq_agent",
    model=LiteLlm(model="groq/llama-3.1-8b-instant"),
    instruction="Say hello in one sentence."
)

async def main():
    session_service = InMemorySessionService()

    runner = Runner(
        app_name="test_app",
        agent=agent,
        session_service=session_service
    )

    # ✅ MUST be awaited
    session = await session_service.create_session(
        app_name="test_app",
        user_id="test_user"
    )

    # ✅ runner.run is NOT async
    for event in runner.run(
        session_id=session.id,
        user_id="test_user",
        new_message=types.Content(
            role="user",
            parts=[types.Part(text="Hello")]
        )
    ):
        if event.content:
            for part in event.content.parts:
                if part.text:
                    print(part.text)
    from litellm.llms.custom_httpx.async_client_cleanup import close_litellm_async_clients
    await close_litellm_async_clients()


if __name__ == "__main__":
    asyncio.run(main())
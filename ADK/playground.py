from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import uuid
import asyncio
from src.agent import root_agent 

async def main():
    session_service = InMemorySessionService()

    # session details
    APP_NAME = 'chatbot'
    USER_ID = 'harshalchalke31'
    SESSION_ID = str(uuid.uuid4())

    # create a stateful session

    stateful_session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
    )

    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service
    )

    # write a user message
    message = types.Content(
        role="user",
        parts=[
            types.Part(
                text=(
"Tell me current time and date. Who are the current President and Vice President of USA?"

                )
            )
        ],
    )
    response = []
    for event in runner.run(
        session_id=SESSION_ID,
        user_id=USER_ID,
        new_message=message

    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    response.append(part.text)

    print("".join(response).strip())

if __name__ == "__main__":
    asyncio.run(main())
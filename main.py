import asyncio 
import logging
import os
from uuid import uuid4
from dotenv import load_dotenv
from vision_agents.core.edge.types import User
from vision_agents.plugins import getstream, openai
from vision_agents.core import agents, cli


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
print("Loaded STREAM_API_KEY:", os.getenv("STREAM_API_KEY"))
print("Loaded OPEN_AI_API_KEY:", os.getenv("OPEN_AI_API_KEY")[:10] + "..." if os.getenv("OPEN_AI_API_KEY") else None)


async def start_agent() -> None:


    llm = openai.Realtime()
    agent = agents.Agent(
        edge = getstream.Edge(),
        agent_user = User(name="My happy AI friends", id="agent"),
        instructions="You're a voice AI assistant. Keep responses short and conversational. Don't use special characters or formatting. Be analytical and helpful.",
        processors=[],
        llm=llm,

    )


    await agent.create_user()
    call = agent.edge.client.video.call("default", str(uuid4()))

    await agent.edge.open_demo(call)

    with await agent.join(call):
        await agent.llm.simple_response("Chat with the user about current stock market")

        await agent.finish()

if __name__ == '__main__':
    asyncio.run(cli.start_dispatcher(start_agent))


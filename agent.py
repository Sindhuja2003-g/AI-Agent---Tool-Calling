from dotenv import load_dotenv
from typing import Any
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, RunContext, function_tool
from livekit.plugins import (
    google,
    cartesia,
    deepgram,
    noise_cancellation,
    silero,
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from tavily import TavilyClient
import os
load_dotenv()


@function_tool()
async def lookup_weather(
    context: RunContext,
    query: str,
) -> dict[str, Any]:
    api_key=os.getenv("TAVILY_API_KEY")
    client = TavilyClient(api_key)
    response=client.search(f"what is the weather in {query}")
    print(query)
    print(response)
    return response

class TavilyAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="Use weather tool to look up current weather in a specific location. Only use it for weather-related questions. Else answer by your own. Reply with perfect emotion tone  and dont read any symbols",
            tools=[lookup_weather]
        )



async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=deepgram.STT(model="nova-3", language="multi"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=cartesia.TTS(model="sonic-2", voice="f786b574-daa5-4673-aa0c-cbe3e8534c02"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
    )

    await session.start(
        room=ctx.room,
        agent=TavilyAgent(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()

    await session.generate_reply(
        instructions="Greet the user and offer your assistance."
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

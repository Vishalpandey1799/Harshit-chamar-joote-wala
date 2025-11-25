import logging
from dotenv import load_dotenv

import tutor_content

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("tutor_agent")
logging.basicConfig(level=logging.INFO)

load_dotenv(".env")

 
agent_state = {
    "mode": "select",
    "current_concept_id": None,
    "current_concept": None,
}


 
def build_system_prompt(mode: str, concept_id: str | None) -> str:
    print(f">>> [PROMPT] building mode={mode}, concept_id={concept_id}")

    if mode == "select":
        return """
You are a tutor coordinator. Ask user:
- Which mode: learn / quiz / teach_back
- Which concept

Then call switch_mode(new_mode, concept_id).
"""

    concept = tutor_content.get_concept_by_id(concept_id)
    if not concept:
        return "Concept not found."

    title = concept["title"]
    summary = concept["summary"]
    question = concept["sample_question"]

    if mode == "learn":
        return f"You are an explainer. Voice=Matthew. Teach: {title}. Summary: {summary}"

    if mode == "quiz":
        return f"You are a quiz master. Voice=Alicia. Ask: {question}"

    if mode == "teach_back":
        return f"You are a reviewer. Voice=Ken. Ask the user to explain {title}"

    return "Unknown mode."

 
class TutorAgent(Agent):
    def __init__(self, mode="select", concept_id=None, tts=None):
        print(f">>> [AGENT INIT] mode={mode}, concept_id={concept_id}, tts_override={tts is not None}")
        self.mode = mode
        self.concept_id = concept_id
        self.custom_tts = tts
        super().__init__(instructions=build_system_prompt(mode, concept_id))

   
    @function_tool
    async def switch_mode(self, ctx: RunContext, new_mode: str, concept_id: str) -> str:
        print(f"\n>>> [MODE SWITCH] new_mode={new_mode}, concept_id={concept_id}")

        valid_modes = ["learn", "quiz", "teach_back"]
        if new_mode not in valid_modes:
            return "Invalid mode."

        concept = tutor_content.get_concept_by_id(concept_id)
        if not concept:
            return "Concept not found."

        # update state
        agent_state["mode"] = new_mode
        agent_state["current_concept_id"] = concept_id
        agent_state["current_concept"] = concept

        # pick Murf voice
        voice_map = {
            "learn": "en-US-matthew",
            "quiz": "en-US-alicia",
            "teach_back": "en-US-ken"
        }
        voice = voice_map.get(new_mode, "en-US-matthew")

        print(f">>> [TTS] building new Murf voice={voice}")
        new_tts = murf.TTS(
            voice=voice,
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True,
        )
 
        print(f">>> [SESSION] Replacing TTS with voice={voice}")
        try:
            ctx.session._tts = new_tts
            print(f">>> [TTS] Successfully set new TTS voice to {voice}")
        except Exception as e:
            print(f">>> [TTS ERROR] Failed to set TTS: {e}")

   
        try:
            ctx.session.update_agent(
                TutorAgent(
                    mode=new_mode,
                    concept_id=concept_id,
                    tts=new_tts
                )
            )
            print(f">>> [AGENT] updated to new mode={new_mode} with voice={voice}")
        except Exception as e:
            print(">>> [AGENT ERROR] failed:", e)

        return f"Switched to {new_mode} for {concept['title']}."


# -------------------------------------------------------------------
# WORKER ENTRYPOINT
# -------------------------------------------------------------------
def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    print("\n>>> [BOOT] Tutor worker starting...")

    initial_voice = "en-US-matthew"
    print(f">>> [BOOT] using starting voice={initial_voice}")

    vad = ctx.proc.userdata["vad"]
 
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(voice=initial_voice),  # only used for initial 'select' mode
        turn_detection=MultilingualModel(),
        vad=vad,
        preemptive_generation=True,
    )

    print(">>> [TTS ENGINE] session.tts =", type(session.tts).__name__)

    await ctx.connect()

    # start with coordinator mode
    await session.start(
        agent=TutorAgent("select", None, tts=murf.TTS(voice=initial_voice)),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

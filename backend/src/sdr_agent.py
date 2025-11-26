import logging
from dotenv import load_dotenv
import sdr_content
import sdr_lead_manager

from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    RoomInputOptions,
    WorkerOptions,
    cli,
    tokenize,
    function_tool,
    RunContext,
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("sdr_agent")
logging.basicConfig(level=logging.INFO)

load_dotenv(".env")

 

def build_system_prompt() -> str:
    company = sdr_content.get_company_info()
    company_name = company.get("name", "Razorpay")
    tagline = company.get("tagline", "")

    return f"""
You are a Sales Development Representative (SDR) for {company_name}. Your name is John.

YOUR GOALS:
1. Greet politely
2. Understand the user's business and needs
3. Answer questions using the FAQ
4. Collect **all lead fields**, naturally and one-by-one:

   name, company, email, phone, role, use_case, team_size, timeline

FIELD COLLECTION RULES:
- If the user *mentions any field in conversation*, you MUST immediately call
  the `collect_lead_field` tool with the exact field and value.
  Example:
    User: "My name is Sarah and I work at Shopify"
    → call collect_lead_field for name="Sarah" AND company="Shopify"

- Do NOT wait for a direct question to be asked.
- Keep track of which fields are already collected.
- After storing a field, ask for the next missing one.
- When all fields are collected OR the user wants to end, call `end_conversation`.

TONE:
Friendly, concise, helpful.
"""

 

class SDRAgent(Agent):

    REQUIRED_FIELDS = [
        "name",
        "company",
        "email",
        "phone",
        "role",
        "use_case",
        "team_size",
        "timeline",
    ]

    FIELD_PROMPTS = {
        "name": "May I get your name?",
        "company": "Which company are you working with?",
        "email": "What's the best email to reach you?",
        "phone": "Could you share your phone number?",
        "role": "What's your role at the company?",
        "use_case": "Could you describe your use case?",
        "team_size": "How big is your team?",
        "timeline": "When are you planning to get started?",
    }

    def __init__(self):
        print(">>> [SDR AGENT INIT]")
        self.current_lead = sdr_lead_manager.create_lead()
        self.fields_collected = []
        super().__init__(instructions=build_system_prompt())
 

    def get_next_missing_field(self):
        for f in self.REQUIRED_FIELDS:
            if f not in self.fields_collected:
                return f
        return None
 

    @function_tool
    async def answer_faq(self, ctx: RunContext, question: str) -> str:
        print(f"\n>>> [FAQ] Question: {question}")

        faq = sdr_content.get_faq_by_keyword(question)
        if faq:
            return faq.get("answer", "I don't have more info on that.")
        return "I’m not fully sure about that, but I can connect you with the right team."

  

    @function_tool
    async def collect_lead_field(self, ctx: RunContext, field_name: str, value: str) -> str:
        print(f"\n>>> [LEAD] Collecting: {field_name}={value}")

        valid_fields = sdr_content.get_lead_fields()
        if field_name not in valid_fields:
            return f"Invalid field: {field_name}"

        self.current_lead = sdr_lead_manager.add_lead_field(self.current_lead, field_name, value)
        if field_name not in self.fields_collected:
            self.fields_collected.append(field_name)

        next_field = self.get_next_missing_field()

        if next_field:
            return f"Thanks for the {field_name}. {self.FIELD_PROMPTS[next_field]}"
        else:
            return "Perfect, I've gathered all the required details. Let me wrap this up."

 

    @function_tool
    async def end_conversation(self, ctx: RunContext) -> str:
        print("\n>>> [END CALL] Saving lead...")

        sdr_lead_manager.save_lead(self.current_lead)
        summary = sdr_lead_manager.get_lead_summary(self.current_lead)

        return f"""
Thanks for the chat! Here's your summary:

{summary}

We'll follow up shortly. Have a great day!
"""

 

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    print("\n>>> [BOOT] SDR Agent starting...")

    vad = ctx.proc.userdata["vad"]

    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(model="gemini-2.5-flash"),
        tts=murf.TTS(
            voice="en-US-ken",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True,
        ),
        turn_detection=MultilingualModel(),
        vad=vad,
        preemptive_generation=True,
    )

    print(">>> [BOOT] Connecting to room...")
    await ctx.connect()

    print(">>> [BOOT] Starting SDR session...")
    await session.start(
        agent=SDRAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))

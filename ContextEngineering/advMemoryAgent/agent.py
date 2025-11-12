from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService
from google.adk.tools import load_memory, preload_memory
from google.genai import types
from google.adk.apps.app import App, ResumabilityConfig


# ==========================================================
# STEP 1 — INITIALIZE Memory & Session Service
# ==========================================================

APP_NAME = "MemoryDemoApp"
USER_ID = "demo_user"

retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504],
)

memory_service = (
    InMemoryMemoryService()
)

session_service = InMemorySessionService()

async def auto_save_to_memory(callback_context):
    """Automatically save session to memory after each agent turn."""
    await callback_context._invocation_context.memory_service.add_session_to_memory(
        callback_context._invocation_context.session
    )


print("✅ Callback created.")

# Agent with automatic memory saving
root_agent = LlmAgent(
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    name="AutoMemoryAgent",
    instruction="Answer user questions.",
    tools=[preload_memory],
    after_agent_callback=auto_save_to_memory,  # Saves after each turn!
)

print("✅ Agent created with automatic memory saving!")
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

# Shared global memory for all sessions
memory_service = (InMemoryMemoryService())
session_service = InMemorySessionService()

print("✅ Step 1: MemoryService initialized")


# ==========================================================
# Create Agent with memory tools
# ==========================================================

root_agent = LlmAgent(
    name="MemoryAgent",
    model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
    instruction=(
        "Answer user questions in simple words. Use load_memory tool if you need to recall past conversations."
    ),
    tools=[load_memory],
)

print("✅ Agent created with memory tools")


# ==========================================================
# STEP 2 — INGEST: Add sessions into memory
# ==========================================================

# We create a reusable session (used by multiple conversations)
session = session_service.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id="shared-session"
)

# Add that session to memory — this links conversation to memory store
memory_service.add_session_to_memory(session)

print("✅ Step 2: Session added to memory (Ingest complete)")


# ==========================================================
# STEP 3 — RETRIEVE: The agent can now use load_memory
# ==========================================================

# The load_memory tool will automatically use memory_service
# when the agent needs to recall facts.

memory_app = App(
    name=APP_NAME,
    root_agent=root_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

print("✅ Step 3: Retrieval ready — load_memory tool will use stored memory")

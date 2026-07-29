"""Run a live ADK demo session (requires GOOGLE_API_KEY in wiki_agent/.env).

Example:
  .\\.venv\\Scripts\\Activate.ps1
  Copy-Item wiki_agent\\.env.example wiki_agent\\.env   # then edit key
  python scripts/adk_demo.py
"""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

# Avoid Windows cp1252 crashes on wiki unicode (°, ≥, ±, etc.)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

load_dotenv(REPO / "wiki_agent" / ".env")

if not os.getenv("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY") == "your-api-key-here":
    print(
        "GOOGLE_API_KEY not set. Copy wiki_agent/.env.example to wiki_agent/.env and add your key.\n"
        "Until then, run: python scripts/offline_demo_ingest.py",
        file=sys.stderr,
    )
    sys.exit(1)


async def main() -> None:
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai import types

    from wiki_agent.agent import root_agent

    app_name = "wiki_agent"
    user_id = "demo_user"
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name=app_name, user_id=user_id, session_id="demo_session"
    )
    runner = Runner(agent=root_agent, app_name=app_name, session_service=session_service)

    prompts = [
        "Ingest all markdown files under raw/seed/ without discussion. Then ingest raw/manuals/sample-ahu-om-excerpt.pdf without discussion.",
        "Why is AHU-3 using 20% more power than its baseline at 75°F outdoor air? Answer only from the wiki. Cite wiki pages. Note contradictions.",
        "Lint the wiki and report findings. Then save the AHU-3 answer as wiki/sessions/ahu-3-high-power-at-75f.md if not already present.",
    ]

    for prompt in prompts:
        print("\n=== USER ===\n", prompt, flush=True)
        content = types.Content(role="user", parts=[types.Part(text=prompt)])
        async for event in runner.run_async(
            user_id=user_id, session_id=session.id, new_message=content
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(part.text, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())

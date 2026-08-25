"""Google ADK agent that refreshes docs/tech from manifest URLs."""

from google.adk.agents import Agent

from .prompts import INSTRUCTION
from .tools.tech_docs import (
    fetch_url,
    list_docs,
    read_file,
    read_manifest,
    update_manifest,
    write_file,
)

root_agent = Agent(
    model="gemini-flash-latest",
    name="docs_fetcher_agent",
    description=(
        "Fetch official tech documentation listed in docs/tech/manifest.yaml "
        "and write markdown snapshots under docs/tech/ for PR review grounding."
    ),
    instruction=INSTRUCTION,
    tools=[
        list_docs,
        read_file,
        read_manifest,
        fetch_url,
        write_file,
        update_manifest,
    ],
)

"""Google ADK agent that refreshes docs/tech from manifest URLs."""

from google.adk.agents import Agent

from .prompts import INSTRUCTION
from .tools.tech_docs import (
    fetch_url,
    inspect_stack,
    list_docs,
    propose_from_project,
    read_file,
    read_manifest,
    sync_manifest_from_project,
    update_manifest,
    write_file,
)

root_agent = Agent(
    model="gemini-flash-latest",
    name="docs_fetcher_agent",
    description=(
        "Sync docs/tech from the host project's dependency files and official doc URLs, "
        "for portable PR review grounding."
    ),
    instruction=INSTRUCTION,
    tools=[
        inspect_stack,
        propose_from_project,
        sync_manifest_from_project,
        list_docs,
        read_file,
        read_manifest,
        fetch_url,
        write_file,
        update_manifest,
    ],
)

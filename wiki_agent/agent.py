"""ADK root agent for the DistrictNex LLM Wiki."""

from google.adk.agents.llm_agent import Agent

from .prompts import INSTRUCTION
from .tools.vault import (
    append_log,
    list_vault,
    read_file,
    read_index,
    read_pdf,
    update_hot,
    write_file,
)

root_agent = Agent(
    model="gemini-flash-latest",
    name="wiki_agent",
    description=(
        "DistrictNex LLM Wiki agent: ingest building-ops sources (markdown + PDF manuals), "
        "maintain an Obsidian wiki, answer from wiki only, and lint for gaps/contradictions."
    ),
    instruction=INSTRUCTION,
    tools=[
        list_vault,
        read_file,
        read_pdf,
        write_file,
        append_log,
        update_hot,
        read_index,
    ],
)

# Google Agent Development Kit — Agents

Canonical: https://google.github.io/adk-docs/agents/

An Agent, or LlmAgent, in Agent Development Kit (ADK) is a self-contained execution unit designed to act autonomously to achieve specific goals. Agents can perform tasks, interact with users, utilize external tools, and coordinate with other agents. The basic components of an Agent are an artificial intelligence (AI) model, task instructions, and optionally, a set of tools to be used by the agent.

## Python Agent Construction

```python
from google.adk import Agent
from google.adk.tools import google_search

agent = Agent(
    name="researcher",
    model="gemini-flash-latest",
    instruction="You help users research topics thoroughly.",
    tools=[google_search],
)
```

## Single Agent to Workflows

In ADK, any agent application that has more than one agent or executable Node is considered a workflow. As tasks and complexity grow, agent workflows allow evolving from a single agent to modular architectures:
- Instruction following performance
- Context limitations
- Agent code modularity
- Mixing deterministic and non-deterministic tasks

## Agent Features

- **AI models**: Swap underlying intelligence by integrating generative AI models from Google and other providers.
- **Pre-built tools and integrations**: Equip agents with tools, plugins, and integrations (web search, MCP tools, databases, APIs).
- **Custom tools**: Create task-specific tools for solving specific problems with precision and control.
- **Artifacts**: Enable agents to create and manage persistent outputs like files, code, or documents.
- **Skills**: Use prebuilt or custom Agent Skills to extend capabilities within context window limits.
- **Plugins**: Integrate complex behaviors and third-party services directly into agent workflows.
- **Callbacks**: Hook into execution lifecycle events for logging, monitoring, or side-effects.

## Repo Review Guidelines

- Expose `root_agent` at the top level of agent packages.
- Return structured dicts (`{"status": ...}`) from tools; do not raise for expected user errors.
- Define strict write sandboxes in agent instructions (e.g. forbid writing to `raw/`).

# Google Agent Development Kit — Tools

Canonical: https://google.github.io/adk-docs/

ADK enables agents to interact with external systems and run custom logic through tools. Tools can be pre-built (e.g., `google_search`) or custom Python callables.

## Defining Custom Tools

ADK wraps Python functions as tools, using the function name, type annotations, and docstrings as the tool schema provided to the model.

```python
def example_tool(query: str) -> dict:
    """Search or process information.

    Args:
        query: The search query string.
    """
    return {"status": "success", "result": f"processed {query}"}
```

## Tool Guidelines

- Use clear docstrings with explicit parameter descriptions (`Args:` section).
- Return JSON-serializable dictionaries containing status and payload (e.g. `{"status": "success", ...}` or `{"status": "error", "error": "..."}`).
- Validate and sanitize input arguments inside tool functions. Enforce filesystem boundaries and path sandboxing.
- Restrict network requests using allowlists, strict timeouts, and size caps.
- Keep side-effects encapsulated within tool functions rather than in model instruction prompts.

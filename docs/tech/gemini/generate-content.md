# Gemini API — Overview and Content Generation

Canonical: https://ai.google.dev/gemini-api/docs

The Gemini API provides access to Google's generative models for text, multimodal inputs, structured outputs, function calling, and conversational agents.

## Authentication

Authenticate using `GOOGLE_API_KEY` (from Google AI Studio or repository secrets). Do not commit API keys to source control.

## Python SDK Usage (`google-genai`)

```python
from google import genai

client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.7-flash",
    input="Explain how AI works in a few words",
)
print(interaction.output_text)
```

### Using generate_content

```python
from google import genai

client = genai.Client(api_key=api_key)
response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="prompt text",
)
text = response.text
```

## Capabilities

- **Structured Outputs**: Constrain responses to JSON schema formats suitable for automated processing.
- **Function Calling**: Connect models to external tools and APIs for agentic workflows.
- **Long Context & Document Understanding**: Ingest large multimodal context, including PDFs, text files, and images.
- **Streaming**: Stream tokens and events in real time.
- **Thinking**: Leverage reasoning and thinking capabilities for complex multi-step tasks.

## Repo Guidelines

- Use `gemini-flash-latest` or latest designated Flash models for standard agent tasks.
- When requesting JSON output, set response schema / mime-types and validate returned structures in application logic.
- Handle empty or truncated responses as explicit errors in CI workflows.

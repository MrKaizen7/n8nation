---
applyTo: ['*.py']
---
# Python Standards for AI Copilot

- Use type hints and dataclasses for structured data.
- Prefer explicit imports; avoid wildcard imports.
- Follow PEP8 for formatting and naming.
- Use docstrings for all functions and classes.
- Integrate with ChromaDB and Google Gemini as per `ai-copilot` workflows.
- For multilingual support, auto-detect language and use smart translation.
- Tag documents by type (webhook, integration, workflow, general) and language.
- Never commit API keys; use `.env` and environment variables.
- See `n8nation/docs/ai-copilot/README.md` for advanced patterns.

---
applyTo: ['n8nation/docs/ai-copilot/*.py']
---
# Integration Patterns for n8n AI Copilot

- Use RESTful APIs for real-time knowledge updates (`update_webhook.py`).
- Document processing must auto-detect language and enrich metadata.
- Integrate vector search via ChromaDB for semantic queries.
- All integrations should support Spanish/English (auto-detect).
- Reference `config.py` for model, DB, and performance settings.
- For external APIs, handle errors gracefully and log updates.
- See `README.md` and `TECHNICAL_SPECS.md` for integration details.

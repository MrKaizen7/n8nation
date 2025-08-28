# N8Nation Enhanced AI Copilot — AI Agent Instructions

## Project Overview
- This repo powers a multilingual AI assistant for n8n workflow automation, with advanced vector search, conversation memory, and real-time knowledge updates.
- Main code lives in `n8nation/docs/ai-copilot/`.

## Architecture & Key Components
- **enhanced_copilot.py**: Main conversational AI, manages memory, context, and prompt engineering.
- **ai-copilot/embed_and_store.py**: Generates multilingual vector embeddings using Google Gemini/text-embedding-004.
- **process_docs.py**: Processes and classifies documents, auto-detects language, enriches metadata.
- **config.py**: Centralized config for models, DB paths, language support, and performance settings.
- **update_webhook.py**: RESTful API for real-time knowledge base updates.
- **ai-copilot/demo_copilot.py**: End-to-end demo, simulates all system features without external dependencies.

## Developer Workflows
- **Setup**: Install Python 3.8+, run `pip install -r requirements.txt` in `ai-copilot`.
- **Environment**: Set `GOOGLE_API_KEY` and other secrets in `.env` (see `.env.example`).
- **Initialize Knowledge Base**:
  ```bash
  python process_docs.py
  python embed_and_store.py
  ```
- **Run Copilot**:
  ```bash
  python enhanced_copilot.py
  ```
- **Update Knowledge**:
  ```bash
  python knowledge_updater.py [--force|--source <name>]
  # Or via webhook: python update_webhook.py
  ```
- **Demo**:
  ```bash
  python demo_copilot.py
  ```
- **Troubleshooting**: See `README.md` for ChromaDB reset, API quota, memory, and language issues.

## Project-Specific Patterns & Conventions
- **Multilingual**: All content, queries, and responses support Spanish/English (auto-detect, smart translation).
- **Conversation Memory**: Recent interactions (10-50) are kept for context; see `ConversationMessage` dataclass.
- **Document Classification**: Documents tagged by type (webhook, integration, workflow, general) and language.
- **Performance**: Tune `EMBEDDING_BATCH_SIZE`, `CHUNK_SIZE`, and `MAX_CONTEXT_LENGTH` in `config.py` for large KBs.
- **Security**: Never commit API keys; use environment variables and `.env` files.
- **Integration**: Example integrations for React and Discord bots in `README.md`.

## External Dependencies
- **Google Gemini API**: For generation and embeddings (API key required).
- **ChromaDB**: Persistent vector DB for semantic search.
- **MkDocs**: Used for documentation site (see `mkdocs-setup/`).

## Key Files & Docs
- `n8nation/docs/ai-copilot/README.md`: Full system guide, troubleshooting, integration examples.
- `n8nation/N8NATION_MASTER_PLAN.md`: Project vision and roadmap.
- `n8nation/TECHNICAL_SPECS.md`: Technical details and specs.
- `n8nation/APP_FEATURES.md`: Feature planning.
- `n8nation/CONTRIBUTING.md`: Contribution guidelines.

---
**For unclear or missing conventions, check the above files or ask for clarification.**

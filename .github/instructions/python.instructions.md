---
applyTo: '*.py'
---
# Python Standards for n8n AI Copilot

## Purpose
Defines robust, actionable standards for Python code in n8n AI Copilot. Ensures consistency, maintainability, and seamless integration with multilingual, context-aware workflows.

## Audience
- Python developers and AI agents contributing to n8n AI Copilot
- New contributors onboarding to the project

## Required Practices
1. **Type Hints & Dataclasses**
   - Use type hints for all function signatures and dataclasses for structured data.
   - Example:
     ```python
     from dataclasses import dataclass
     @dataclass
     class ConversationMessage:
         content: str
         timestamp: datetime
         language: str
     ```
2. **Imports**
   - Prefer explicit imports; avoid wildcard imports for clarity and maintainability.
3. **Formatting & Naming**
   - Follow PEP8 for code style, naming, and formatting.
   - Use snake_case for variables/functions, PascalCase for classes.
4. **Documentation**
   - Use docstrings for all functions and classes. Include purpose, parameters, and return types.
5. **Integration Patterns**
   - Integrate with ChromaDB and Google Gemini as per `ai-copilot` workflows.
   - Reference `integration.instructions.md` for API and DB usage.
6. **Multilingual Support**
   - Auto-detect language and use smart translation for all user-facing content.
   - Tag documents by type (webhook, integration, workflow, general) and language.
7. **Security**
   - Never commit API keys; use `.env` and environment variables.
8. **Testing & Error Handling**
   - Write tests for all new features. Handle errors gracefully and log issues.

## Content Guidelines
- Include code examples and command snippets where relevant.
- Use Markdown links to reference other instruction files and documentation.
- Maintain a professional, clear, and welcoming tone.

## References
- [n8nation/ai-copilot/README.md](../../n8nation/ai-copilot/README.md)
- [integration.instructions.md](./integration.instructions.md)
- [CONTRIBUTING.md](../CONTRIBUTING.md)
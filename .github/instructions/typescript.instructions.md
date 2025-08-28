---
applyTo: '*.ts'
---
# TypeScript Standards for n8n AI Copilot

## Purpose
Defines robust standards for TypeScript code in n8n AI Copilot, ensuring strict typing, documentation, and multilingual/context-aware logic.

## Audience
- TypeScript developers and AI agents contributing to n8n AI Copilot
- New contributors onboarding to the project

## Required Practices
1. **Strict Typing & Interfaces**
   - Use strict typing and interfaces for all workflow components.
   - Example:
     ```typescript
     interface WorkflowNode {
       id: string;
       type: string;
       config: object;
     }
     ```
2. **Documentation**
   - Document all exported functions and classes with JSDoc comments.
3. **Multilingual & Context-Aware Logic**
   - Follow project conventions for multilingual support and context-aware automation.
   - Reference `integration.instructions.md` for integration patterns.
4. **Component Generation & Review**
   - Use prompts for intelligent component generation and code review.
   - Reference `generate-intelligent-component.prompt.md` for best practices.

## Content Guidelines
- Include code examples and command snippets where relevant.
- Use Markdown links to reference other instruction files and documentation.
- Maintain a professional, clear, and innovative tone.

## References
- [integration.instructions.md](./integration.instructions.md)
- [generate-intelligent-component.prompt.md](../prompts/generate-intelligent-component.prompt.md)
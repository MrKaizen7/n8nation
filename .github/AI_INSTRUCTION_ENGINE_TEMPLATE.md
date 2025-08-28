# AI Instruction Engine Template for Repositories

This template provides a clear, adaptable structure for implementing an AI instruction and prompt system in any codebase. It enables teams to guide AI coding agents (like GitHub Copilot) with project-specific context, standards, and workflows, regardless of the underlying tech stack or architecture.

---

## 1. Purpose

The `.github` instruction engine is a set of files and conventions that:
- Provide high-level and detailed guidance to AI agents working in the repository
- Standardize prompts for code generation, review, and scaffolding
- Ensure instructions and prompts are always up-to-date with the codebase
- Enable both human and AI contributors to maintain project consistency

---

## 2. Recommended Folder Structure

```
.github/
├── copilot-instructions.md         # Main guide for AI agents (project overview, key patterns, workflows)
├── instructions/                   # Detailed, modular instruction files
│   ├── <language>.instructions.md  # Language-specific standards (e.g., python.instructions.md)
│   ├── <framework>.instructions.md # Framework-specific guides (e.g., react.instructions.md)
│   ├── <feature>.instructions.md   # Feature/architecture-specific guides
│   └── ...
└── prompts/                        # Reusable, task-specific prompt files
    ├── <task-name>.prompt.md       # Prompts for code generation, review, scaffolding, etc.
    └── ...
```

---

## 3. File Types & Content Guidelines

### 3.1. `copilot-instructions.md`
- Project summary and goals
- Key architectural patterns and workflows
- Critical conventions (naming, error handling, testing, etc.)
- How AI agents should interact with project files and context
- Links to detailed instruction files

### 3.2. Instruction Files (`.instructions.md`)
- Language, framework, or feature-specific standards
- Code style, best practices, and anti-patterns
- Error handling, testing, performance tips
- Integration points and gotchas
- Should be modular and easy to update

### 3.3. Prompt Files (`.prompt.md`)
- Task-specific instructions for AI agents
- Code generation, review, scaffolding, documentation, etc.
- Reference relevant instruction files for standards
- Use variables (e.g., `${selection}`, `${file}`) for context-aware responses
- Should be reusable and easy to adapt

---

## 4. Maintenance & Best Practices

- Update instruction and prompt files whenever codebase changes affect standards, workflows, or architecture
- Encourage AI agents to propose updates if discrepancies are detected
- Use changelogs and roadmaps to track major changes and completed tasks
- Keep instructions modular for easy adaptation to new features or tech
- Document the instruction engine in the project README for onboarding

---

## 5. Example Usage

- AI agent reads `copilot-instructions.md` for project context
- For a Python backend, agent consults `instructions/python.instructions.md` for code style
- When generating a React component, agent uses `prompts/generate-component.prompt.md` referencing `instructions/react.instructions.md`
- After major changes, agent updates `CHANGELOG.md` and proposes edits to instructions

---

## 6. Adaptation Checklist

- [ ] Create `.github/copilot-instructions.md` with project overview and key patterns
- [ ] Add modular instruction files for each language, framework, and feature
- [ ] Add prompt files for common AI-assisted tasks
- [ ] Document the instruction engine for contributors
- [ ] Keep all files synchronized with codebase changes

---

This template can be copied, customized, and extended for any repository to enable a robust, maintainable AI instruction engine that empowers both human and AI contributors.

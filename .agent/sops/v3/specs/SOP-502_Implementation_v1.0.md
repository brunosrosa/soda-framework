# SOP-502: Implementation Standards

**Phase:** Execution (Phase 5)
**Role:** Code Agent / Developer

## Context
Code is read more often than it is written. Optimize for readability.

## Standards
1.  **Language:** Python (Backend/AI), TypeScript (Frontend).
2.  **Style:** PEP8 (Python), Prettier (TS).
3.  **Docs:** Docstrings are mandatory for public methods.
4.  **Error Handling:** Fail fast. Don't swallow exceptions silently.

## Special Rules
- **Configuration:** Use `pydantic` or `.env`. Never globals.
- **Logging:** Use `structlog` or standard `logging`. No `print()`.
- **Async:** Prefer async/await for I/O bound tasks.

## Checklist
- [ ] Is it readable?
- [ ] Is it testable?
- [ ] Is it secure?

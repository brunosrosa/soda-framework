---
description: Create project plan using Planning-With-Files skill (Manus pattern). Creates task_plan.md, findings.md, progress.md.
---

# /plan - Planning With Files (SODA Integrated)

$ARGUMENTS

---

## 🟢 Context & Skill Activation

**Applying knowledge of `@[skills/planning-with-files]`...**

> **Objective:** Transform the user's request ($ARGUMENTS) into a structured 3-File Plan (Manus Pattern).

---

## 📂 File Protocol (SODA Clean Root)

You MUST create/update these 3 files in **`.agent/memory/hot/`**:

1.  **`task_plan.md`**: The Roadmap.
2.  **`findings.md`**: Knowledge Base (If new task, start empty/template).
3.  **`progress.md`**: Execution Log (If new task, start empty/template).

---

## 🤖 Execution Steps

1.  **Analyze Request**: Understand `$ARGUMENTS`.
2.  **Load Templates**: Read `.agent/skills/planning-with-files/references/`.
3.  **Generate Plan**:
    *   Synthesize the goal into `task_plan.md` (Phases, Status).
    *   Initialize `findings.md` with any initial context/requirements.
    *   Initialize `progress.md` with "Session Start" entry.
4.  **Review**: Ensure paths are correct (`.agent/memory/hot/`).
5.  **Output**: Confirm creation to user.

---

## 🔍 Socratic Check (Before Writing)

If the request is vague (e.g., "/plan build system"), **STOP** and ask clarifying questions first.
Only proceed to write files when the goal is clear enough to define Phases 1-3.

---

## Example Output

```text
✅ **Plan-With-Files Initialized**

📂 **Memory Context created in `.agent/memory/hot/`**:
- `task_plan.md`: [Defined 4 Phases for $ARGUMENTS]
- `findings.md`: [Initialized]
- `progress.md`: [Log Started]

READY to execute Phase 1. Run `/start` or begin tool use.
```

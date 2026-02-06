# PROJECT CHARTER (PID-Context)

## 1. IDENTITY & MISSION
- **Project Name:** SODA (Spec-Oriented Dockerized Architecture) Framework.
- **Mission:** Create the definitive "Agentic Operating System" for neurodivergent developers (AH/SD + ADHD).
- **Core Value:** Externalize executive function. Transform software development from an art form ("Vibe Coding") into a deterministic industrial process ("Cognitive Assembly Line").
- **Target Audience:** Developers who struggle with working memory and task initiation but excel at high-speed problem solving.

## 2. NON-GOALS (What we are NOT building)
- **NOT a Chatbot Wrapper:** We are not building a UI for ChatGPT. We are building a headless OS that *uses* LLMs.
- **NOT for Junior Devs:** SODA assumes the user knows how to code but needs help with *process* and *focus*.
- **NOT SaaS:** SODA must run locally or on user-controlled infrastructure (Sovereignty).

## 3. TECHNOLOGY STACK (Hardware-Safe Constraint)
> **CRITICAL:** Local GPU (RTX 3070 Mobile) has a broken fan. Zero-load policy on local GPU.

- **Orchestration (The Brain):** Google Gemini Pro (Latest) via Cloud API.
- **Agents Runtime (The Hands):** `smolagents` (Python) running on local CPU.
- **Memory:** `OpenMemory` (GraphDB) + Markdown Files (`task_plan.md`).
- **Isolation:** Docker MCP Gateway.

## 4. PROTOCOLS (The Laws)
1.  **Clean Root Axiom:** Project root allows ONLY `PROJECT_CHARTER.md` and `src/`. All operational files live in `.agent/`.
2.  **Spec-Lock Protocol:** No code (Phase 6) without approved Spec (Phase 2/4).
3.  **Flow Integrity:** Outputs from Phase N are read-only inputs for Phase N+1.
4.  **Hardware Safety:** If `SODA_LLM_PROVIDER` == `ollama`, warn user about heat risk.

## 5. AUTHORITY MATRIX
- **Architecture Decisions:** Requires user verification via `ARC` protocol.
- **Implementation:** Autonomous within defined specs (Ralph Loop MAX_ITERS=15).
- **Release:** Manual approval required (Human-in-the-Loop).
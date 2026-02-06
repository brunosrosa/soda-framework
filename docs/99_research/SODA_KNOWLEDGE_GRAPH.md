# SODA KNOWLEDGE GRAPH & EVOLUTION LOG

**Version:** 1.8 (Hardware Agnostic Enterprise Edition)
**Last Update:** 06/fev/2026 (Bruno Add, probably dont have time to update)
**Status:** Frozen for Implementation.

---

## 1. EVOLUTION LOG (The Why)

### v1.0 -> v1.4 (The "Standard" Era)
- **Focus:** Estabelecer a estrutura de pastas e fases (Kanban Tatico).
- **Limit:** Dependência excessiva de prompts manuais e "Copy/Paste".

### v1.5 -> v1.7 (The "Tool" Experiments)
- **Hypothesis:** "Aleph (RLM) é o futuro da pesquisa profunda."
- **Findings:**
    - Aleph é recursivo. Uma pergunta gera 50 requisições.
    - **Fatal Flaw:** Inviável para usuários de CLI com cotas rígidas (1500 req/dia ou menos). Risco de DoS auto-infligido.
- **Pivot:** Abandonar Aleph como "Cérebro". Rebaixá-lo a "Ferramenta de Leitura" (se usado) ou substituí-lo.

### v1.8 (The "Sovereign & Agnostic" Era)
- **Core Change:** **Code-as-Policy** (Smolagents).
    - Em vez de JSON instável, o agente escreve Python.
    - Python roda **localmente** (CPU).
    - Resultado: 1 Requisição = Múltiplos passos lógicos. Eficiência de cota de 10x.
- **Hardware Agnosticism:**
    - O sistema não assume mais GPU disponível.
    - O sistema não assume mais Cloud ilimitada.
    - Ele pergunta ao `.env`.

---

## 2. TOOLCHAIN DEFINITIVE (The "Super-Stack" v1.8)

### A. The Brain (Provedor de Inteligência)
*Configurável via `SODA_LLM_PROVIDER`*
1.  **Google Gemini Pro (Latest/Preview):**
    -   **Role:** Big Brain (Architecture, Planning, Reasoning).
    -   **Why:** Janela de contexto massiva (2M+), raciocínio de ponta (Gemini 3 Class), custo zero via OAuth/Antigravity.
2.  **Google Gemini Flash (Latest/Preview):**
    -   **Role:** Fast Brain (Tool usage, micro-tasks).
    -   **Why:** Baixa latência.
3.  **Ollama (Local - Qwen 2.5/Phi-4):**
    -   **Role:** Fallback / Privacy Mode.
    -   **Constraint:** **DESATIVADO POR PADRÃO (POR HORA)** (Ventoinha da GPU quebrada).
    -   **Future:** Ativar quando hardware for reparado.

### B. The Engine (Executor)
1.  **Smolagents (Hugging Face):**
    -   **Role:** O Runtime do Agente.
    -   **Mechanism:** `CodeAgent`. O LLM escreve scripts Python que são executados em um sandbox local.
    -   **Crucial:** Permite loops, condicionais e variáveis sem chamar o LLM a cada linha.

### C. The Eyes (Ingestion & Perception)
1.  **Docfork (Container):**
    -   **Role:** Conversão sanitizada (Web -> Markdown). Previne "prompt injection" via HTML sujo.
    -   **Priority:** Primary.
2.  **Rtfmbro (Container):**
    -   **Role:** Leitura profunda de repositórios e manuais técnicos.
3.  **Heuristic-MCP:**
    -   **Role:** Busca semântica local + Call Graph. Superior ao `grep` para code navigation.

### D. The Brain & Hands (Orquestração & Execução)
-   **Ralph Loop (v1.7):** Motor de persistência OODA (CPU-bound via `Smolagents`).
-   **Docker MCP Gateway:** Segmentação modal (Research vs Coding vs Audit). Isolamento de rede e filesystem.
-   **OpenMemory:** Memória episódica (GraphDB) para decisões arquiteturais e preferências.

---

## 3. PROJECT GENESIS & PHILOSOPHY (The "Why")

### Identity
-   **Stage:** **GENESIS** (Implementação do SODA v1.7.2).
-   **Goal:** Criar o "Exocórtex" para desenvolvedores neurodivergentes (AH/SD + TDAH).
-   **Strategy:** "Line of Assembly Cognitive". Transformar desenvolvimento em engenharia determinística.
    -   **Clean Root Axiom:** A raiz contém APENAS `PROJECT_CHARTER.md` e `src/`. Todo o resto em `.agent/`.
    -   **Spec-Lock Protocol:** Nenhum código (Fase 6) sem Spec aprovada (Fase 2/4).
    -   **Flow Integrity:** Outputs de Fases anteriores são imutáveis para Fases posteriores.

### Evolution Log (Context)
-   **v1.0 - v1.4:** Fundação dos axiomas (Clean Root, Ralph Loop, 22 SOPs).
-   **v1.5:** Convergência de Ag-Kit + BMAD + Gateway.
-   **v1.7.2 (DEFINITIVE TARGET):** "The Master Architecture".
    -   Unificação total em `.agent/` (Kernel).
    -   **Hardware-Safe:** CPU-only para agentes locais, Cloud LLM para raciocínio.
    -   **Super-Stack:** Docfork, Heuristic-MCP, OpenMemory, GitHub PM.

### Structure Analysis (Target vs Current)
-   **Target (v1.7.2):**
    -   `.agent/` (Kernel Unificado)
        -   `/config` (Gateway, Master Rule)
        -   `/memory` (Hot/Cold)
        -   `/sops_registry` (Os 22 SOPs)
        -   `/workflows` (Gatilhos)
        -   `/skills` (Meta-Skills)
    -   `.openspec/` (Specs Técnicas)
-   **Current State:** Esqueleto fragmentado (`.agent`, `.soda`).
    -   **Action:** Refatorar para estrutura v1.7.2. Absorver `.soda` em `.agent`.

### Environment Strategy
-   **`.env.example`:** Deve refletir a 'Super-Stack' v1.7.2 (chaves para Exa, Tavily, Gemini, Docker config).

## 4. HARDWARE CONSTRAINTS (Critical)

> **⚠ WARNING: BROKEN GPU FAN ⚠**

- **Symptoms:** Se a GPU for estressada (ex: rodar Qwen 72B local), o sistema superaquece e desliga.
- **Directive:**
    - **NÃO** instale ou configure Ollama para *inferência pesada* agora.
    - **USE** APIs Cloud (Gemini) para todo o processamento pesado.
    - **PERMITA** que scripts leves (Python puro, Regex, AST parsing) rodem na CPU local.

## 4. ARCHITECTURE AXIOMS

1.  **Cleaner Root:** Raiz = `PROJECT_CHARTER.md`, `src/`, `docker-compose.yml`. Tudo o resto em `.agent/`.
2.  **Spec-Lock:** 22 SOPs garantem que nada é codado sem spec.
3.  **Flow Integrity:** Fases são unidirecionais.

---

## 5. BATTLE PLAN SUMMARY (Bootstrap)

1.  Validar ambiente Python (`uv`).
2.  Popular `PROJECT_CHARTER.md` (Constituição).
3.  Popular `.agent/sops_registry/` (Os 22 SOPs).
4.  Implementar `.agent/scripts/ralph_loop.py` (O Motor Smolagents).
5.  Criar `.env` com switch de provedor.

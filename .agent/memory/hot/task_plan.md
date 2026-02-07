# PLANO TÁTICO SODA (O Motor)

> **STATUS:** 🔴 PENDENTE DE CONFIGURAÇÃO (TOOLS)
> **FASE:** 0 - BOOTSTRAP & TOOLING

## 🛠️ FASE 0: FUNDAÇÃO & FERRAMENTAS (Setup)
*Antes de rodar a esteira, precisamos ligar as máquinas.*
- [ ] **Setup-01**: Instalar Kernel & CLI (`setup_tools.sh`).
- [ ] **Setup-02**: Subir Docker Services (`OpenMemory`).
- [ ] **Setup-03**: Integrar "Swarm de Ferramentas" (Ag-Kit, GitHub, BMAD, Smolagents, OpenMemory, OpenSpec, ARC Protocol, Plan-With-Files, MCPs, RLM, Ralph, Searchs, etc).

## 🟢 FASE 1: FUNDAÇÃO (Negócio & Linguagem)
- [ ] **SOP-01**: Regras de Negócio (BRD) `[Docs: docs/business/rules.md]`
- [ ] **SOP-02**: Linguagem Ubíqua (Glossário) `[Docs: docs/business/glossary.md]`

## 🔵 FASE 2: PRODUTO (Definição)
- [ ] **SOP-03**: Requisitos de Produto (PRD) `[Docs: docs/product/prd.md]`
- [ ] **SOP-04**: Critérios de Aceite (Gherkin) `[Docs: docs/product/specs.feature]`

## 🎨 FASE 3: DESIGN (UX/UI)
- [ ] **SOP-05**: Fluxos de Usuário (Mermaid) `[Docs: docs/design/flows.mmd]`
- [ ] **SOP-06**: Escrita UX & Voz `[Docs: docs/design/voice.md]`
- [ ] **SOP-07**: Alinhamento de Design System `[Docs: docs/design/system.md]`

## 🏗️ FASE 4: ARQUITETURA (Engenharia)
- [ ] **SOP-08**: Contratos de API (OpenAPI) `[spec: .openspec/api/swagger.yaml]`
- [ ] **SOP-09**: DDR - Design de Dados `[spec: .openspec/db/schema.mmd]`
- [ ] **SOP-10**: Modelagem de Ameaças (Segurança) `[spec: .openspec/security/threats.md]`

## ⚔️ FASE 5: PLANEJAMENTO TÁTICO (Sharding)
- [ ] **SOP-11**: Quebra de Tarefas (Github Issues / PM MCP) `[Output: Matrix Traceability]`

## 💻 FASE 6: CONSTRUÇÃO (O Build)
- [ ] **SOP-12**: Loop de Implementação (Ralph/Smolagents) `[Src: src/]`
- [ ] **SOP-13**: Gestão de Segredos `[Sec: .env]`
- [ ] **SOP-14**: Auto-Documentação `[Docs: README.md]`

## 🧪 FASE 7: VERIFICAÇÃO (Qualidade)
- [ ] **SOP-15**: Geração de Testes (E2E/Unit) `[Tests: tests/]`
- [ ] **SOP-16**: Auditoria de Análise Estática `[Report: audit.log]`

## 🚀 FASE 8: RELEASE (Operações)
- [ ] **SOP-17**: Migrações de Banco de Dados `[SQL: migrations/]`
- [ ] **SOP-18**: Pipelines CI/CD `[Ops: .github/workflows]`
- [ ] **SOP-19**: Setup de Observabilidade `[Ops: monitoring]`
- [ ] **SOP-20**: Compliance & I18n `[Docs: compliance.md]`
- [ ] **SOP-21**: RCA & Postmortem `[Docs: ops/rca.md]`
- [ ] **SOP-22**: Notas de Release `[Docs: CHANGELOG.md]`

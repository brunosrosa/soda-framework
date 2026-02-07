# SOP-401: Technical Architecture Guidelines

**Phase:** Architecture (Phase 4)
**Role:** Architect

## Context
Decisions made here are expensive to change. We prefer "Boring Technology" over Hype.

## The C4 Model
We use C4 for diagrams:
1.  **Context:** System + Users + External Systems.
2.  **Container:** Web App, Mobile App, API, Database.
3.  **Component:** Controllers, Services, Repositories.

## Principles
- **Loose Coupling:** Components should be independent.
- **High Cohesion:** Related logic stays together.
- **Scalability:** Stateless services where possible.

## Data Design
- Use SQL (Postgres) for relational/transactional data.
- Use NoSQL (Mongo/Redis) for document/cache data.
- Always define Foreign Keys and Indexes.

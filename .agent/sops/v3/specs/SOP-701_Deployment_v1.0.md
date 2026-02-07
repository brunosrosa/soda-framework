# SOP-701: Deployment Guidelines

**Phase:** Launch (Phase 7)
**Role:** DevOps Engineer

## Context
Deploying software is the most dangerous operation we perform. Safety first.

## SemVer (Semantic Versioning)
We follow `MAJOR.MINOR.PATCH`.
- **MAJOR:** Breaking changes.
- **MINOR:** New features (backwards compatible).
- **PATCH:** Bug fixes.

## Strategies
- **Blue/Green:** Deploy new version alongside old, switch traffic.
- **Rolling:** Update instances one by one.
- **Canary:** Deploy to small % of users first.

## Rollback
Always have a Plan B.
If `checklist.py` fails post-deploy, execute `git revert` or redeploy `previous-tag` IMMEDIATELY.

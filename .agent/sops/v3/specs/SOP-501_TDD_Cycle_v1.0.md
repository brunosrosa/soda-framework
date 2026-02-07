# SOP-501: Test Driven Development (Cycle)

**Phase:** Execution (Phase 5)
**Role:** Code Agent / Developer

## Context
TDD is non-negotiable for complex logic in SODA. It prevents regression and documents intent.

## The Cycle
1.  **Red:** Write a failing test. It should fail for the right reason (assertion error, not syntax error).
2.  **Green:** Make it satisfy the test. Simplicity > Elegance here.
3.  **Refactor:** Clean up. The tests are your safety net.

## Best Practices
- **Naming:** Test names should be sentences (e.g., `test_user_cannot_login_without_password`).
- **Isolation:** Tests should not depend on external APIs (Mock them).
- **Speed:** Unit tests must run in milliseconds.

## Troubleshooting
- If tests pass but feature fails E2E -> Check Integration SOP.
- If tests are "flaky" -> Check for race conditions or unclosed resources.

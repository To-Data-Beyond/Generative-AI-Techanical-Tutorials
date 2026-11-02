---
paths:
  - "app/api/**/*.py"
---

# Backend API Rules

- Every endpoint includes request and response schemas.
- Keep business logic in services and route handlers thin.
- Never expose internal exception details in API responses.

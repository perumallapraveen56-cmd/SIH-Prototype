# Security Policy & Vulnerability Disclosure

**Project**: SIH26017 — Predictive Analytics System for Early Detection of Land Acquisition Delays  
**Team**: NEXORA_TAU  
**Scope**: Public Deployment Security Guidelines & Hygiene  

---

## 🛡️ 1. Security Architecture & Controls

The SIH26017 platform implements defense-in-depth security principles across application, network, and data layers:

1. **Authentication & Session Security**:
   - Industry-standard **JSON Web Tokens (JWT)** signed via **HMAC-SHA256 (HS256)**.
   - Passwords hashed using **bcrypt** with salted work factors ($2^{12}$ iterations).
   - Sessions expire after a configurable duration (`ACCESS_TOKEN_EXPIRE_MINUTES`).

2. **Role-Based Access Control (RBAC)**:
   - Dedicated role enforcement (`Admin`, `Officer`, `Analyst`).
   - Route-level dependency injection (`get_current_user`, `has_role`) protects sensitive operations and mutation endpoints.

3. **Input Validation & Sanitization**:
   - Strict Pydantic v2 schemas for all incoming API payloads.
   - SQL Injection protection through SQLAlchemy ORM parameterized queries.
   - Cross-Site Scripting (XSS) prevention via Angular DOM sanitization and context-aware interpolation.

4. **Information Disclosure & Error Hardening**:
   - Global exception handling in FastAPI catches all unhandled exceptions and outputs sanitized error envelopes with zero stack traces or internal filenames.

5. **Secret Hygiene & Environment Separation**:
   - Zero hardcoded passwords, tokens, or private keys in source code.
   - All sensitive credentials loaded from runtime environment variables (`.env`).
   - `.gitignore` prevents inadvertent commits of configuration, virtual environments, local database caches, or secrets.

---

## 🔑 2. Credential Rotation Guidance

If a credential is ever suspected to be compromised in staging or production:

1. **JWT Secret Key Rotation**:
   - Generate a new 256-bit random key:
     ```bash
     openssl rand -hex 32
     ```
   - Update `SECRET_KEY` in the environment configuration (`.env`).
   - Restart the backend server. All active tokens are immediately invalidated, requiring users to re-authenticate.

2. **Database Password Rotation**:
   - Change user credentials on the PostgreSQL database server.
   - Update the connection string `DATABASE_URL` in the server `.env`.
   - Perform a rolling restart of the application backend.

3. **User Password Rotation**:
   - Admins can update user records via standard password hashing functions or CLI maintenance scripts.

---

## 📢 3. Reporting a Vulnerability

If you identify a security vulnerability or sensitive information exposure within this repository:

1. **DO NOT file a public issue on GitHub.**
2. Send a detailed report to the security team:
   - **Email**: `security@nexora.gov.in` (or project maintainer)
   - Include: affected endpoints, steps to reproduce, and impact assessment.
3. The maintainers will acknowledge receipt within 48 hours and coordinate a secure patch release.

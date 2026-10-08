# Security Policy

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them privately using one of the following methods:

### Preferred: GitHub Security Advisories

1. Go to the [Security Advisories](https://github.com/wild8highlander/Trivortex/security/advisories) page
2. Click **"New advisory"**
3. Fill in the details of the vulnerability
4. Submit as **"Private"** — this creates a confidential channel with the maintainer

### Alternative: Email

Send a detailed report to [aslan08_05@mail.ru](mailto:aslan08_05@mail.ru) with the subject line:

```text
[SECURITY] trivortex / Trivortex: <brief description>
```

### What to Include

- **Description** of the vulnerability and its impact
- **Steps to reproduce** the issue (code snippet, proof of concept)
- **Affected versions** — which version(s) are vulnerable
- **Suggested fix** — if you have one
- **Your contact information** — for follow-up questions

---

## Response Timeline

| Stage | Timeline |
|-------|----------|
| **Acknowledgment** | Within 48 hours of report |
| **Initial assessment** | Within 5 business days |
| **Status update** | Every 7 days until resolved |
| **Fix for critical** | Within 7 days |
| **Fix for high** | Within 14 days |
| **Fix for medium/low** | Within 30 days |
| **Public disclosure** | After fix is released and users have had time to update |

---

## Security Features

This repository employs multiple layers of security:

### Automated Scanning

| Tool | Frequency | Scope |
|------|-----------|-------|
| **CodeQL** | Every push + weekly | Python, C++, JavaScript |
| **OpenSSF Scorecard** | Weekly | Full repository |
| **Dependabot** | Weekly | All dependencies |
| **Dependency Review** | Every PR | New dependencies |
| **Pre-commit hooks** | Every commit | Private keys, large files, merge conflicts |

### Supply Chain Security

- **Pinned action versions** — All GitHub Actions use SHA-pinned references
- **Minimal permissions** — Workflows use least-privilege `permissions:` blocks
- **Harden Runner** — Uses `step-security/harden-runner` for CI hardening
- **Dependency lockfile** — All Python deps pinned in `pyproject.toml`

### Code Integrity

- **Signed commits** — Recommended for all contributors
- **Branch protection** — `main` branch requires PR review + passing CI
- **Pre-commit hooks** — Automated code quality enforcement on every commit

---

## Security Best Practices for Contributors

1. **Never commit secrets** — API keys, tokens, passwords, or private keys
2. **Use environment variables** — For any sensitive configuration
3. **Pin dependencies** — Specify exact versions in requirements
4. **Review your diffs** — Before every commit, check for accidentally included secrets
5. **Report responsibly** — Follow coordinated disclosure (see above)

---

## Known Security Considerations

- **Numerical precision**: Some verification computations use floating-point arithmetic. Results should be independently verified with arbitrary-precision libraries (mpmath, Arb) for security-critical applications.
- **Proof assistant trust**: Formal verification relies on the correctness of the proof assistant's kernel. Lean 4, Coq, and Isabelle all have small, audited trusted computing bases, but no system is provably bug-free.
- **Supply chain**: Third-party dependencies (NumPy, SciPy, LAPACK) are trusted. Critical results should be verified with independent implementations.

---

## OpenSSF Scorecard

[![OpenSSF Scorecard](https://api.securityscorecards.dev/projects/github.com/wild8highlander/Trivortex/badge)](https://securityscorecards.dev/viewer/?uri=github.com/wild8highlander/Trivortex)

We continuously monitor our security posture using the [OpenSSF Scorecard](https://securityscorecards.dev). Current scores are available at the link above.

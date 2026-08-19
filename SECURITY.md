# Security Policy

py-ABAC is an access-control library: a vulnerability here can mean a policy
that should deny access instead allows it, so security reports are taken
seriously and prioritized over regular bug reports.

## Supported Versions

py-ABAC does not yet maintain parallel release branches. Security fixes are
made against the latest released minor version; users on older versions
should upgrade to get a fix.

| Version | Supported          |
| ------- | ------------------ |
| 0.4.x   | :white_check_mark: |
| < 0.4   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub
issues, discussions, or pull requests.**

Preferred: use GitHub's private reporting for this repository —
[Report a vulnerability](https://github.com/ketgo/py-abac/security/advisories/new)
(also reachable from the repo's **Security** tab → **Advisories** → **Report a
vulnerability**). This opens a private advisory visible only to maintainers
until a fix is ready.

If you're unable to use GitHub's private reporting, email
[ketangoyal1988@gmail.com](mailto:ketangoyal1988@gmail.com) with the subject
line `[py-abac security] <short summary>`.

Please include as much of the following as you can:

- A description of the vulnerability and its potential impact (e.g. a
  crafted policy or request that bypasses an intended deny, a condition that
  causes catastrophic backtracking/DoS, an injection vector in a storage
  backend, unsafe deserialization of policy JSON).
- Steps to reproduce, or a minimal PoC (example policy/request JSON and the
  code exercising it).
- The affected version(s) and storage backend, if relevant.
- Any known mitigation or workaround.

### What to expect

- **Acknowledgement** within 5 business days of your report.
- An initial assessment of severity and whether it's accepted, along with an
  expected timeline, within 10 business days.
- Regular updates while a fix is in progress, at least every 2 weeks.
- Credit in the release notes/advisory once the fix ships, unless you'd
  prefer to remain anonymous.
- If a report is declined (e.g. not reproducible, out of scope, or working
  as intended), an explanation of why.

We ask that you give us a reasonable opportunity to fix the issue before any
public disclosure, and we'll coordinate a disclosure date with you once a
fix is available.

### Scope

In scope: the `py_abac` package itself — policy parsing (`Policy.from_json`),
condition evaluation, target matching, the PDP evaluation algorithms, and the
bundled storage backends (`memory`, `file`, `mongo`, `sql`, `redis`).

Out of scope: vulnerabilities in third-party dependencies (report upstream),
and issues requiring an already-compromised policy store or an attacker who
can already author policies with the privileges you're trying to protect.

Thank you for helping keep py-ABAC and its users safe.

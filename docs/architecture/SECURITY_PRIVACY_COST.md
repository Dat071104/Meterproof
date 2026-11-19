# Security, resource and cost boundaries

1. **Secrets:** NEVER accept external users' management keys into public SaaS, logs, git, prompts, bug reports or shared fixtures. Owner-local provider analytics, if used, runs with owner-controlled credentials on local machine.
2. **Tenant security:** private API auth, tenant derived server-side, least privilege per table/read model; T12 must prove writes/reads cannot cross tenants.
3. **Data provenance:** `PRODUCTION`, `PILOT`, `SANDBOX`, `SYNTHETIC` separated; retention/deletion policy; sample fixtures sanitized. No personal/payment data unless absolutely necessary and authorized.
4. **Public UI:** read-only and sanitized, no arbitrary upload/import keys. User-provided exports processed **locally** by Lite.
5. **AI tools:** allowlisted read-only methods only, typed IDs and scopes; forbid DB writer/remote shell; retrieved text is untrusted; adverse prompt-injection evals required.
6. **Infra:** local Docker permitted only as instructed by active milestone; paid API tests and cloud provisioning require explicit cost ceiling and approval first. No recurring paid resources without ownership, monitor and teardown.
7. **WAL retention:** monitor replication slot lag, data volume and disk; a dead CDC consumer can retain WAL. Tests must include recovery and cleanup.
8. **Operational assurance:** health/readiness, lag, DLQ, checkpoint, sink retries, report version conflicts, incident metrics. Logs reference IDs and hashes, never credentials, raw prompts or invoice PII.
9. **Git safety:** preserve existing workspace pack, `.gitignore`, CI and project code. No destructive install, force-push or deletion by automation.

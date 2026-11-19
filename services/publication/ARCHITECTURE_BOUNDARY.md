# services/publication — module boundary (PLANNED, NOT IMPLEMENTED)

**Milestone:** P3 · **Ownership:** Authoritative versioned CAS publication writer.

**Non-negotiable:** Only Core owns immutable report versions and publication pointer; transaction/fencing prevents stale writer; support rollback-pointer without erasing old versions.

**Verification responsibility:** tests/integration + T05/T09.

This marker preserves a clean intended repository structure for Codex. It is not a claim that code, runtime or tests already exist. Follow the active milestone and inspect actual existing project source before adding implementation.

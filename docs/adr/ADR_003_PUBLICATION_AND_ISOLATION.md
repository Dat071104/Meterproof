# ADR-003 — Immutable report versions, CAS publication, consumer isolation

**Status:** Proposed for G0. **Decision:** candidate results in isolated namespaces, verification before publish, immutable versioned reports, CAS/fencing current pointer. Lite local outputs are not Core reports; Atlas reads versioned, sanitized Core API with no writer credentials. **Reason:** unsafe partial corrections and AI-generated claims cannot overwrite financial history. **Tradeoff:** additional DB/control-plane complexity. **Tests:** T05/T09/T12, AI non-interference.

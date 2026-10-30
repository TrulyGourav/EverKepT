# ADR-0003: Cryptographic primitives and libraries

Status: proposed (AEAD choice to be confirmed in Phase 1)

## Decision
Use only maintained libraries: `cryptography`, `argon2-cffi`, PyNaCl, `shamir-mnemonic`. Argon2id for passphrases, HKDF-SHA256 for derivation, X25519 sealed boxes, Ed25519 signatures, SLIP-39 for secret sharing. Every serialized object carries `format_version` and `alg_id`.

## Open question
XChaCha20-Poly1305 (large random nonces, simple chunking) versus AES-256-GCM (hardware acceleration, WebCrypto availability for the v1 browser client). Leaning to AES-256-GCM with per-chunk derived nonces if the browser client is a firm v1 goal; otherwise XChaCha20-Poly1305. Decide with a small spike and known-answer tests.

## Consequences
No custom primitives. All derivations get published known-answer tests. Property tests (Hypothesis) cover round-trips, tamper detection and AAD swap/rollback rejection.

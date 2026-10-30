# ADR-0001: Zero-knowledge, client-side cryptography

Status: accepted

## Context
Confidentiality from platform administrators is a core product requirement. Server-side envelope encryption with a KMS would let a compromised server or admin with KMS access read data.

## Decision
All encryption, key derivation, signing and share reconstruction happen in the client. The server stores ciphertext, wrapped keys, verifiers and workflow state only. The MVP client is a Python CLI/SDK; a browser client (WebCrypto/WASM) follows in v1.

## Consequences
- Forgetting the passphrase and recovery key loses the vault; the platform cannot help.
- No server-side search, preview or OCR.
- Conditional release needs split-key custody (ADR-0004), because the owner is absent at release time.
- A compromised client sees plaintext; this is out of scope.

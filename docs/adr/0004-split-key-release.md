# ADR-0004: Split-key conditional release, no platform escrow

Status: accepted

## Context
If the owner is absent at release time, someone other than the owner must hold key material that completes decryption. Options compared in the design: pre-sealing with a policy gate, split-key, custodian Shamir, proxy re-encryption, time-lock, identity-based encryption, enclave escrow, blockchain.

## Decision
Per rule, the owner client creates a release key split with SLIP-39 into Share-P (platform custody, wrapped by KMS, released only by the workflow) and Share-R (recipient custody). Registered recipients (M1) receive Share-R sealed to their public key. Unregistered recipients (M2) use a Claim Secret from a Claim Kit; the server verifies possession through a signature, never seeing the secret. **No platform escrow in the MVP.** An opt-in, explicitly non-zero-knowledge escrow mode may be considered in a later version.

## Consequences
- The platform alone cannot decrypt; the recipient alone cannot decrypt before release.
- Platform plus recipient collusion can release early in the MVP; mitigations arrive in v1 (HSM/TEE policy, guardian shares, anchored audit).
- If the platform disappears, release is impossible until the escape share (v1) exists.
- A recipient with neither an account nor a claim secret cannot be supported.

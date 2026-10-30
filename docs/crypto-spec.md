# Cryptographic specification (draft v0)

Status: draft for Phase 1 implementation. Nothing here is hand-rolled; primitives come from `cryptography`, `argon2-cffi`, PyNaCl and `shamir-mnemonic`. Every serialized object carries `{format_version, alg_id}` so algorithms can change.

## Primitives
| Purpose | Primitive |
|---|---|
| Passphrase KDF | Argon2id (parameters recorded per account) |
| Key derivation | HKDF-SHA256 with explicit `info` labels |
| Content and key wrapping | XChaCha20-Poly1305 (via PyNaCl) or AES-256-GCM; one chosen in ADR-0003 |
| Key agreement / sealing | X25519 sealed box |
| Signatures | Ed25519 |
| Secret sharing | SLIP-39 Shamir via `shamir-mnemonic` |
| Hashing | SHA-256 (BLAKE3 optional later) |

## Key hierarchy
```
passphrase --Argon2id--> MK
  MK --HKDF "auth"--> auth key   (server stores a verifier only)
  MK --HKDF "wrap"--> KEK_owner
recovery key (256-bit random) also wraps VK
VK (random) wraps: identity private keys (X25519, Ed25519) and item keys
item key (random 256-bit, stable per item)
  version subkey = HKDF(item key, "ver" || version)
content = chunked AEAD, AAD = item_id || version || chunk_index || alg_id || final_flag
```
Filenames, MIME types and tags live inside the encrypted manifest. Blob sizes are padded to buckets.

## Release package (per rule)
1. Client generates release key RK (256-bit).
2. `item_key_wrapped = AEAD(RK, item_key)` for each covered item.
3. RK is split with SLIP-39: scheme `{threshold: 2, shares: 2}` in the MVP (P, R); `scheme_id` recorded so 2-of-3 (escape share) and k-of-n guardian schemes are a configuration change.
4. Share-P is wrapped by the platform KMS key and stored server-side. It is released only by the release service when the workflow state allows.
5. Share-R is protected per recipient mode:
   - **M1:** sealed box to the recipient's X25519 public key (pinned fingerprint).
   - **M2:** AEAD under `claim_wrap_key` (see below).
6. The owner Ed25519-signs the manifest `{item_id, version, content_hash, metadata_hash, rule_hash, timestamp}`.

## Claim Secret (M2)
- `claim_secret`: 192 bits from the OS CSPRNG, encoded as 18 checksummed words. Optional PIN is hardened with Argon2id and appended to the IKM.
- `prk = HKDF-Extract(salt=claim_id, ikm=claim_secret[||pin_hash])`
- `ctx = claim_id || rule_id || owner_fingerprint || identity_profile_hash`
- `claim_wrap_key = HKDF-Expand(prk, "wrap" || ctx)`; `claim_auth_seed = HKDF-Expand(prk, "auth" || ctx)` seeds an Ed25519 key. The server stores only the public verifier.
- Redemption: server issues a challenge (nonce bound to session, claim id, workflow id, short TTL); client signs it; first valid proof plus identity match binds the claim to the recipient account. Consumption is two-phase (bind, then adoption receipt).

## Audit log
Entry hash = SHA-256(previous_hash || canonical_json(entry)). Periodic Merkle root is published to an `AnchorPort` (stub in MVP; OpenTimestamps or RFC 3161 later).

## Open items for ADRs
- AEAD choice (ADR-0003).
- Argon2id parameters and upgrade path.
- Canonical serialization format for signed objects.
- Padding bucket sizes.
- Test vectors: publish known-answer tests for every derivation above.

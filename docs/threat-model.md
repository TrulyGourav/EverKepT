# Threat model (Phase 0)

## Assets
1. Plaintext of vault items and their metadata (names, types, tags).
2. Key material: passphrase, recovery key, vault key, item keys, release keys, Share-P, Share-R, claim secrets.
3. Integrity of rules and of the release decision (a wrongly released item cannot be recalled).
4. Audit history.
5. Availability of release over decades.

## Trust boundaries
- **Client** (CLI/SDK): trusted with plaintext and keys. A compromised client is out of scope.
- **API + DB + blob store**: untrusted for confidentiality; trusted only for availability and for enforcing the release gate.
- **Release service + KMS adapter**: holds Share-P; the most sensitive server component.
- **Notification channels** (email/SMS): untrusted, used for alerts and invitations only, never to carry key material.

## Adversaries and controls
| # | Adversary | Goal | Controls | Residual risk |
|---|---|---|---|---|
| T1 | External attacker with DB + blob access | Read data | Client-side AEAD, wrapped keys, encrypted metadata | Metadata (counts, padded sizes, timing) |
| T2 | Malicious admin | Read data or force a release | No decryption material server-side; Share-P released only by workflow state; 4-eyes for overrides; hash-chained, anchored audit | Admin plus colluding recipient |
| T3 | Account-takeover attacker | Redirect or cancel rules | Step-up auth, edit delay, out-of-band alerts, signed rule versions | Attacker holding passphrase and second factor |
| T4 | Fake heir | Trigger a release | Inactivity only makes a transfer eligible; cooling-off with owner veto; recipient verification; claim secret; attempt budget | Stolen kit plus impersonated identity (needs KYC, v1) |
| T5 | Malicious server substituting recipient keys | Read items sealed to a recipient | Fingerprint pinning, owner-visible key changes | User skips verification |
| T6 | Platform and recipient collusion | Early release | Owner-visible audit, anchoring; v1: HSM/TEE policy, guardian shares | Accepted in MVP, documented |
| T7 | Phishing of recipient | Capture claim secret | Secret never transmitted; official client only | User types it into a lookalike client |
| T8 | Future cryptanalysis | Harvest now, decrypt later | Algorithm ids, rewrap tooling, PQ hybrid roadmap | X25519/Ed25519 until PQ hybrid |
| T9 | Operator error or provider loss | Data or release loss | Ciphertext backups, versioned blobs, recovery drills; v1 escape share and export bundle | Platform disappearance in MVP |
| T10 | Bug causing premature release | Early release | Injectable clock, idempotent transitions, state-machine property tests, timers freeze during outages | Residual logic bugs |

## Abuse cases to test (carried into Phase 4)
- DB dump contains no plaintext, filenames, or usable keys.
- Share-P cannot be obtained before `RELEASED`.
- Editing an audit row breaks chain verification.
- A stolen session cannot change a rule without step-up.
- A background token refresh does not reset the inactivity clock.
- A second claimant on a bound claim lands in `DISPUTED`.
- Platform downtime does not count as owner inactivity.

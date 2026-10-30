# Architecture

Modular monolith, hexagonal. One FastAPI service and one worker process; module boundaries are enforced by review and (planned) import-linter rules. See ADR-0002.

## Modules (`src/everkept/`)
| Module | Responsibility |
|---|---|
| `identity` | accounts, authentication, sessions, recipient key directory |
| `vault` | items, versions, encrypted blob metadata, signed manifests |
| `keys` | wrapped-key records, release-share custody, `KmsPort` |
| `policy` | transfer rules, triggers, eligibility policies |
| `release` | durable workflow state machine |
| `verification` | evidence, attestations, `ProofingPort` |
| `audit` | hash-chained log, anchoring port |
| `notify` | notification ports, escalation ladders |
| `platform` | config, clock, DB, observability |

## Ports (adapters live outside the domain)
`KmsPort`, `BlobStorePort`, `NotifierPort`, `ProofingPort`, `AnchorPort`, `Clock`.

## Trigger model
`Trigger.evaluate(ctx) -> Signal`; `EligibilityPolicy` combines signals into `Eligibility`; the release engine consumes only `Eligibility` plus safeguards. Guardian attestation is a later signal source (ADR-0005).

## Client/server split
All encryption, key derivation, signing and share reconstruction run in the client (`clients/`, added in Phase 1). The server stores ciphertext, wrapped keys, verifiers and workflow state only.

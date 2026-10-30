# ADR-0002: Modular monolith with ports and adapters

Status: accepted

## Context
The MVP is built by one or two developers. Microservices would add distributed-systems cost with no MVP benefit.

## Decision
One FastAPI service plus one worker process, organised into modules (`identity`, `vault`, `keys`, `policy`, `release`, `verification`, `audit`, `notify`, `platform`). External dependencies sit behind ports (KMS, blob store, notifier, proofing, anchoring, clock). Cross-module imports go through each module's public interface; import-linter rules will enforce this once modules have content.

## Consequences
Modules can be extracted later along existing seams. Boundary discipline relies on tooling and review.

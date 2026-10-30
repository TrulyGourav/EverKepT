# EverKepT

Rule/config-based data transfer: a zero-knowledge vault where each item can carry a policy describing when, how and to whom it is released, including when the owner is unavailable.

**Status:** Phase 0 (foundations). No vault or release functionality yet.

## Docs
- [Architecture](docs/architecture.md)
- [Threat model](docs/threat-model.md)
- [Cryptographic specification (draft)](docs/crypto-spec.md)
- [Architecture decision records](docs/adr/)

## Development
Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
make install   # create env, install deps
make up        # Postgres, MinIO, Mailpit
make check     # ruff + mypy
make test
make run       # API at http://localhost:8000/docs
```

## Principles
1. The platform never holds anything that lets it decrypt on its own.
2. Inactivity is never treated as death; it can only make a transfer *eligible*, after safeguards.
3. All time-dependent logic uses an injected `Clock`.
4. No hand-rolled cryptography.

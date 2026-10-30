# ADR-0005: Inactivity makes a transfer eligible, never "deceased"

Status: accepted

## Decision
The inactivity trigger emits only an `OwnerUnresponsive` signal. The system never records or displays "deceased". The strongest state is `ELIGIBLE`, reached only after the check-in ladder, reminders, a cooling-off period with owner veto, and (before release) recipient verification and a final notice window. Veto remains possible until `RELEASED`.

Triggers produce signals; an `EligibilityPolicy` combines them; the release engine consumes only `Eligibility` plus safeguards. Guardian attestation (v1) is added as another signal source and evidence requirement without changing the engine.

## Rules
- Only interactive strong-auth events and explicit check-ins reset the clock; background refreshes and automation do not.
- Platform outages freeze or reset timers.
- Production enforces minimum delays; demo mode (shortened timers) is refused when `env=prod`.
- All time comes from an injected `Clock`.

## Consequences
Wrongful release is made hard at the cost of slower legitimate release. Product copy, API names and audit entries use "eligible", never "deceased".

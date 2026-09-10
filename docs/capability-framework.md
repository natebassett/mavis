# Capability Framework

## Purpose

The capability framework is MAVIS's stable boundary between the assistant core and anything it may eventually use: simulated devices, smart-home adapters, voice services, model providers, or developer tools.

Phase 2 intentionally provides contracts and registration only. It does not connect MAVIS to physical hardware, a cloud provider, or a local language model.

## Core concepts

| Contract | Responsibility |
| --- | --- |
| `Capability` | Abstract adapter that executes a bounded family of actions. |
| `CapabilityRequest` | Immutable request containing the capability, action, input parameters, context, identifier, and timestamp. |
| `CapabilityResult` | Immutable terminal result correlated to its originating request. |
| `CapabilityConfiguration` | Immutable per-capability settings, including whether it is enabled. |
| `CapabilityRegistry` | Registers adapters, validates configuration, routes requests, and checks result correlation. |

## Lifecycle

```text
Create request
      ↓
Registry validates capability and configuration
      ↓
Enabled capability executes request
      ↓
Registry verifies result correlation
      ↓
Return terminal result
```

The forthcoming action-lifecycle and safety-policy features will sit around this framework. They will decide whether an action is allowed or needs confirmation before it is sent to a capability.

## Contract rules

- Capability and action identifiers are canonical lower-case strings containing letters, numbers, underscores, or hyphens.
- Requests, results, configurations, and their top-level mappings are immutable after creation.
- All timestamps are timezone-aware and normalised to UTC.
- A capability result must preserve the request identifier, capability name, and action name.
- A disabled capability returns a typed rejected result without executing its adapter.
- Duplicate registration is rejected unless replacement is explicitly requested.

## Adding a capability

```python
from app.capabilities import Capability, CapabilityRequest, CapabilityResult


class ExampleCapability(Capability):
    @property
    def name(self) -> str:
        return "example"

    def execute(self, request: CapabilityRequest) -> CapabilityResult:
        if request.action != "run":
            return CapabilityResult.unsupported(request, "Action is not supported.")

        return CapabilityResult.succeeded(request, "Example action completed.")
```

Register it during application composition, not inside the capability itself:

```python
registry.register(ExampleCapability())
```

## Error behaviour

The framework raises domain-specific exceptions for malformed requests, registration mistakes, unknown capabilities, execution failures, and broken adapter contracts. Expected action outcomes should normally be represented as a `CapabilityResult` with a status such as `rejected`, `failed`, or `unsupported`.

## Non-goals

- No device implementation or model runtime is included.
- No policy engine, approval UI, audit store, or planner is included yet.
- No capability can execute a real-world action until later features introduce it behind explicit safety controls.

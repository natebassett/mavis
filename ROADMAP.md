# MAVIS Product Roadmap

## Purpose

This roadmap defines the software-first path for MAVIS: a local-first personal assistant platform that can be developed on current hardware, then deployed to an always-on home server when suitable hardware is available.

It is a living plan, not a promise to build every idea at once. Every phase must finish with a useful, tested outcome that remains valid in later phases.

## Design commitments

- **Privacy and local control:** keep personal data and core operations local where possible.
- **Safe action boundaries:** the language model or planner proposes actions; permissioned, deterministic code validates and performs them.
- **Hardware independence:** write against interfaces and test against simulations before connecting real hardware.
- **Replaceable intelligence:** model providers, prompts, retrieval, and future adapters are versioned components, not the MAVIS core.
- **Incremental delivery:** finish narrow vertical slices instead of building disconnected feature collections.

## Delivery model

MAVIS uses a phase-based feature-branch workflow. It keeps the stable product line protected while allowing the active phase to evolve through small, reviewable changes.

```text
main                         Stable, release-ready history
└── p2/sandbox               Active Phase 2 integration branch
    └── p2/<feature>         Focused, short-lived feature branch
```

The same convention applies to later phases, for example `p3/<feature>` and `p4/<feature>`.

### Branch responsibilities

| Branch | Responsibility |
| --- | --- |
| `main` | Contains only validated, release-ready milestones. Each completed phase is merged here. |
| `p<phase>/<integration>` | Integrates tested features for one active phase; currently `p2/sandbox`. |
| `p<phase>/<feature>` | Contains one coherent, independently reviewable outcome and its tests. |

### Feature quality gate

Before a feature branch merges into its phase integration branch, it must:

1. Have a narrow written purpose and avoid unrelated changes.
2. Include automated tests or documented validation appropriate to the feature.
3. Update relevant documentation, configuration examples, or migration notes.
4. Pass the phase integration checks.
5. Be reviewed through a pull request, including self-review when MAVIS is a solo project.

Feature branches are created from the current phase integration branch and merged back promptly. Avoid opening dependent branches at the same time; begin the next one after its prerequisite has reached the integration branch.

---

## Phase 1 — MAVIS Kernel

**Goal:** establish the dependable software foundation of MAVIS.

### Current scope

- [x] Repository setup, `.gitignore`, and environment configuration.
- [x] Application logging and configuration manager.
- [x] Console background runtime.
- [x] Orchestrator shell.
- [x] Intent types, routing, confidence, and unknown-intent fallback.
- [x] SQLite memory database and preference storage.
- [x] Semantic embeddings and semantic memory search.
- [x] Agent-message type and in-process message bus.

### Exit criteria

- The foundation is documented, repeatable to set up, and protected from sensitive-data commits.
- Core modules have clear responsibilities and do not depend on future hardware.

---

## Phase 2 — MAVIS Sandbox

**Goal:** make MAVIS a safe, demonstrable assistant in a completely simulated environment.

### Scope

- [ ] Define capability interfaces for action execution, model responses, device state, and structured execution results.
- [ ] Implement a capability registry, shared error types, and configuration validation.
- [ ] Implement a simulated household: rooms, users, lights, locks, scenes, and routine device states.
- [ ] Add an action lifecycle: plan, validate, request approval, execute, and record a result.
- [ ] Add risk classification, permission rules, confirmation flows, dry-run mode, and an emergency stop.
- [ ] Add a timestamped audit/event trail with human-readable explanations and correlation identifiers.
- [ ] Add resettable simulation state, deterministic time, scenario fixtures, and simulated failure modes.
- [ ] Define a `ModelProvider` boundary with a fake scripted implementation; do not add a real LLM runtime yet.
- [ ] Define the memory-context boundary needed by actions; richer personal memory remains Phase 3 work.
- [ ] Connect the orchestrator to intent, memory, and simulated capabilities.
- [ ] Create a formal automated unit, integration, and acceptance test suite.
- [ ] Establish a text-command interaction loop with useful help, status, and diagnostic output.

### Planned delivery streams

Phase 2 is intentionally split into focused feature branches. Each stream includes its own tests and documentation, then merges into `p2/sandbox` before the next dependent stream begins.

| Order | Feature branch | Outcome | Depends on |
| ---: | --- | --- | --- |
| 1 | `p2/capability-framework` | Stable contracts for capabilities, requests, results, errors, and registration. | MAVIS Kernel |
| 2 | `p2/test-harness` | Test layout, fixtures, scenario conventions, and integration checks. | MAVIS Kernel |
| 3 | `p2/digital-home` | Simulated rooms, users, devices, scenes, and deterministic state changes. | Capability framework, test harness |
| 4 | `p2/action-lifecycle` | Structured planning, validation, execution, and result handling. | Capability framework, digital home |
| 5 | `p2/safety-policy` | Risk levels, confirmations, permissions, dry-run, and emergency-stop rules. | Action lifecycle |
| 6 | `p2/audit-events` | Inspectable event history, explanations, and action correlation. | Action lifecycle, safety policy |
| 7 | `p2/simulation-tools` | State reset, deterministic clock, fixtures, and fault injection. | Digital home, test harness |
| 8 | `p2/model-provider-contract` | Replaceable model interface and a fake scripted provider for tests. | Capability framework |
| 9 | `p2/memory-contract` | Explicit action-to-memory context and storage boundary. | Capability framework |
| 10 | `p2/diagnostics` | Health/status output, configuration checks, and developer diagnostics. | Action lifecycle, audit events |

The initial sequence is deliberate: it creates the shared contracts and quality infrastructure before behaviour is added. This allows real devices, voice, model runtimes, dashboards, and future coding tools to replace adapters rather than restructure the assistant core.

### Exit criteria

- MAVIS safely completes at least 20 documented text-command scenarios against simulated devices.
- Every state-changing action has a recorded decision, approval state, result, and simulated target.
- The scenario suite covers success, refusal, cancellation, invalid input, and simulated-device failure paths.
- Simulation state can be reset and scenarios can be replayed deterministically.
- The phase integration branch passes all automated checks without microphones, speakers, local models, or smart-home hardware.

---

## Phase 3 — MAVIS Mind

**Goal:** give MAVIS reliable, understandable personal context without relying on a physical deployment or a local LLM.

### Scope

- [ ] Create an editable memory model with source, confidence, retention, and correction history.
- [ ] Build explicit preference and routine data structures.
- [ ] Add reminders, schedules, and planning data structures.
- [ ] Add local document-ingestion and retrieval interfaces with test data.
- [ ] Define MAVIS's personality and response rules as version-controlled configuration.
- [ ] Give the user visibility and control over stored personal information.

### Exit criteria

- A user can inspect, correct, and remove stored information.
- Context is drawn from explicit, traceable records rather than opaque or silent assumptions.

---

## Phase 4 — MAVIS Interfaces

**Goal:** prepare MAVIS to interact with a person and a home while retaining fully simulated development paths.

### Scope

- [ ] Define adapters for text, voice input, speech output, displays, and notifications.
- [ ] Model listening, muted, deafened, and manual-override states.
- [ ] Define a household model: users, rooms, device capabilities, and permission levels.
- [ ] Build Home Assistant/Matter integration boundaries and simulated implementations.
- [ ] Define online-provider interfaces and offline/fallback behaviour.
- [ ] Test wake and voice flows with synthetic events and recorded fixtures only where consented.

### Exit criteria

- The core behaves identically when using simulated interfaces or a future real adapter.
- No microphone, speaker, device, or cloud account is required to verify the phase.

---

## Phase 5 — MAVIS Product

**Goal:** make the software operable, maintainable, and safe to release before it reaches a real home server.

### Scope

- [ ] Create a private local API and administrative dashboard.
- [ ] Add user roles, secret handling, settings validation, and permission management.
- [ ] Add scheduling, health checks, structured audit logs, and diagnostics.
- [ ] Add data migrations, export/delete controls, and backup/restore procedures.
- [ ] Add release packaging, configuration profiles, upgrade checks, and rollback procedures.
- [ ] Version prompts, capability configurations, and future model configurations.

### Exit criteria

- A new instance can be configured, validated, upgraded, backed up, and restored predictably.
- Significant actions, configuration changes, and failures are observable and diagnosable.

---

## Phase 6 — MAVIS Home

**Goal:** deploy MAVIS to always-on hardware and connect the tested software to the real world.

### Scope

- [ ] Provision the home server and secure its local network access.
- [ ] Run a suitable local model through Ollama or another supported runtime.
- [ ] Connect approved microphones, speakers, and real device adapters.
- [ ] Integrate selected smart-home services and device protocols.
- [ ] Tune latency, reliability, energy use, privacy controls, and recovery behaviour.
- [ ] Establish a staged update process with model/configuration evaluation and rollback.

### Exit criteria

- MAVIS runs reliably as an always-on, local-network service.
- Real-world actions follow the same permission and audit rules proven in simulation.

---

## Phase 7 — MAVIS Developer

**Goal:** add a capable coding assistant after suitable model hardware is available.

### Scope

- [ ] Connect a capable local model provider to the previously defined model interface.
- [ ] Add workspace-aware code retrieval and task sessions.
- [ ] Add permissioned tools for reading files, producing patches, running tests, and inspecting diffs.
- [ ] Add coding-task evaluations, regression checks, and model/configuration comparisons.
- [ ] Support versioned model prompts, retrieval settings, and optional fine-tuning adapters.
- [ ] Add an approval-first workflow for modifications, commands, and Git operations.

### Exit criteria

- MAVIS can complete a defined set of coding tasks in a repository, with all changes reviewable and reversible.
- Changes in model, prompt, tool, or adapter behaviour are evaluated before promotion.

---

## Long-term research and optional expansion

These are deliberately outside the critical path:

- Foundation-model training from scratch.
- Full autonomous task delegation.
- Mobile, smart-mirror, smart-glasses, and wearable experiences.
- Distributed local AI networking.
- Advanced multi-user voice authentication.

They may be promoted into a future phase only after the preceding system is stable and the required hardware, privacy model, and safety controls are understood.

## Scope review process

At the end of each phase:

1. Confirm the exit criteria with real evidence.
2. Record deferred work rather than quietly adding it to the next milestone.
3. Reassess priorities, available hardware, and privacy/safety requirements.
4. Update this roadmap before beginning the next phase.

This keeps MAVIS ambitious without turning it into an unbounded project.

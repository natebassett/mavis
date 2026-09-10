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

- [ ] Define capability interfaces for action execution, model responses, and device state.
- [ ] Implement a simulated household: rooms, lights, locks, and routine device states.
- [ ] Add action planning, risk classification, confirmations, and an audit log.
- [ ] Connect the orchestrator to intent, memory, and simulated capabilities.
- [ ] Create a formal automated test suite and scenario fixtures.
- [ ] Establish a text-command interaction loop with useful help and status output.

### Exit criteria

- MAVIS safely completes at least 20 documented text-command scenarios against simulated devices.
- Every state-changing action has a recorded decision, result, and simulated target.
- The scenario suite runs without microphones, speakers, local models, or smart-home hardware.

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

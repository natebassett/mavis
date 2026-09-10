# MAVIS

> A local-first personal assistant platform, built software-first and designed to become an always-on home assistant.

MAVIS (Multi-functional Artificial Virtual Intelligence System) is a long-term engineering project to create a private, extensible assistant that can grow from a dependable local software runtime into a home-hosted system. The project begins with the software foundations that can be built and tested today; dedicated hardware, voice endpoints, local models, and real smart-home devices are added only when they are available.

The goal is not to imitate a chatbot. MAVIS is being designed as a maintainable assistant platform with memory, explicit permissions, modular capabilities, and a controlled path to local AI models and home integration.

## Project status

MAVIS is in its foundation stage. The current repository contains a working Python baseline, not a finished assistant.

Implemented today:

- Configuration loading from environment variables.
- Structured application logging.
- A console-based background runtime.
- A basic orchestrator shell.
- Keyword intent routing with confidence and fallback results.
- SQLite-backed memories and preferences.
- Semantic memory embeddings and similarity search.
- An in-process message bus and agent-message type.

Not yet implemented:

- An LLM integration or local Ollama deployment.
- Tool execution, permission policies, or simulated devices.
- Voice input/output, wake-word detection, and speaker recognition.
- A web/dashboard interface, real smart-home integration, or an always-on server deployment.

The detailed, living plan is in [ROADMAP.md](ROADMAP.md).

## Product direction

MAVIS is intended to become:

- **Local-first:** personal data, memory, and core operations stay under the owner's control wherever possible.
- **Safe by design:** high-impact actions require explicit approval and leave an auditable record.
- **Modular:** capabilities such as models, voice, device control, and integrations are replaceable adapters rather than hard-coded dependencies.
- **Software-first:** simulated interfaces and automated checks are built before physical hardware is required.
- **Evolvable:** code, prompts, tools, model configurations, and future fine-tuning adapters can be versioned, evaluated, upgraded, and rolled back.

The eventual home deployment may use a local model runtime such as Ollama. MAVIS will own the assistant experience around a chosen model—its tools, memory, policies, knowledge, and update process—rather than depend on training a frontier language model from scratch.

## Development milestones

1. **MAVIS Kernel** — dependable architecture, storage, routing, and boundaries.
2. **MAVIS Sandbox** — a typed, fully simulated assistant with safe action planning and tests.
3. **MAVIS Mind** — editable memory, routines, preferences, planning data, and personal context.
4. **MAVIS Interfaces** — simulated contracts for voice, rooms, devices, displays, and integrations.
5. **MAVIS Product** — dashboard/API, operations, backups, monitoring, update, and rollback workflows.
6. **MAVIS Home** — deployment to real always-on hardware, local models, and home devices.
7. **MAVIS Developer** — a later coding-assistant capability, added once suitable model hardware is available.

Each milestone has a defined outcome and remains useful after later hardware is added. See [ROADMAP.md](ROADMAP.md) for scope and acceptance criteria.

## Architecture

```text
Input adapters (typed now; voice later)
                |
          MAVIS runtime
                |
   Orchestration and intent routing
          |                 |
     Memory layer      Capability adapters
     (SQLite +         (simulated now; real
      semantic search)  devices/models later)
                |
       Logs, settings, and audit records
```

The central rule is simple: MAVIS core code talks to capability interfaces, not directly to a microphone, model, light, lock, or cloud service. A simulated implementation can therefore be used during development and replaced by a real adapter later.

The concrete Phase 2 contract is documented in [docs/capability-framework.md](docs/capability-framework.md).

## Repository layout

```text
app/
  config/       Environment-based configuration
  core/         Runtime, orchestration, messaging
  intent/       Intent types and routing
  memory/       SQLite storage and semantic memory utilities
  utils/        Shared utilities, including logging
tests/          Current development checks and examples
docs/           Architecture and public contract documentation
main.py         Console entry point
ROADMAP.md      Product roadmap and scope controls
```

## Getting started

Prerequisites: Python 3.11 or later is recommended.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python main.py
```

The current runtime accepts text in the terminal. Enter `exit`, `quit`, or `shutdown` to stop it.

The files in `tests/` are currently development checks and examples. A formal automated test suite is a required outcome of the MAVIS Sandbox phase.

## Configuration and privacy

Copy `.env.example` to `.env` and keep `.env` private. Do not commit API keys, local databases, recordings, voice profiles, personal logs, or credentials.

Current configuration values include:

| Variable | Purpose |
| --- | --- |
| `MAVIS_ENV` | Selects the runtime environment. |
| `LOG_LEVEL` | Sets application log verbosity. |
| `DATABASE_PATH` | Sets the local SQLite memory database path. |
| `WAKE_WORD` | Reserves the wake phrase setting for future voice support. |
| `OPENAI_API_KEY` | Reserved for an optional future provider; it is not required by the current runtime. |

## Scope discipline

MAVIS is deliberately ambitious, so additions must protect its foundation:

- Complete a small end-to-end slice before beginning a broad new subsystem.
- Keep physical-world effects behind explicit, tested permission checks.
- Treat the roadmap as a living document: revise scope at phase boundaries, then record the decision.
- Keep “train a foundation model from scratch” outside the critical path. Local models, retrieval, adapters, and evaluation provide meaningful ownership without blocking the platform.

## Author

Nathaniel Bassett — Software Engineering & Data Science

# Lumon Severed Floor Operations Terminal

A deliberately fallible Flask service for demonstrating Sentry Autofix, Seer, and the Sentry VS Code extension. It models the internal APIs behind Lumon's severed floor: Macrodata Refinement, Optics and Design, Security, Wellness, incentives, payroll, the Perpetuity Wing, and more.

The app includes 30 deterministic production-style failures. Twenty-nine originate in [`src/lumon/services/severed_floor.py`](src/lumon/services/severed_floor.py), making that file particularly useful for asking the extension questions such as:

> Are there any bugs in `src/lumon/services/severed_floor.py`?

The defects are intentionally part of the application. Do not fix them before the demo, no matter what Mr. Milchick says.

## Quick Start

Requires Python 3.11 or newer.

```bash
cd lumon-terminal
make setup
make generate
```

`make generate` invokes the app in-process, triggers all 30 failures, flushes the Sentry transport, and exits. A successful run ends with:

```text
Completed: 30/30 error events generated.
```

The local `.env` is preseeded with the same local Sentry DSN previously used by `flask-error`, so no shell exports are needed. Update `LOCAL_SENTRY_DSN` in `.env` if the local project or tunnel changes. The file is gitignored to keep future credentials out of source control; `.env.example` documents the supported settings.

## Sentry Configuration

The app automatically loads `.env` from the `lumon-terminal` project root. DSNs are selected in this order:

1. `SENTRY_DSN`, when present
2. `LOCAL_SENTRY_DSN`
3. The existing local `flask-error` DSN as a development fallback

Set `SENTRY_DSN` to an empty value to disable event delivery, as the test command does.

| Variable | Default | Purpose |
| --- | --- | --- |
| `LOCAL_SENTRY_DSN` | Existing local error-gen project | Local Sentry destination |
| `SENTRY_DSN` | Unset | Explicit override, including hosted Sentry |
| `SENTRY_ENVIRONMENT` | `development` | Event environment |
| `SENTRY_RELEASE` | `lumon-terminal@1.0.0` | Release attached to events |
| `SENTRY_TRACES_SAMPLE_RATE` | `1.0` | Transaction sampling |
| `SENTRY_PROFILES_SAMPLE_RATE` | `0.0` | Profile sampling |

The SDK also attaches a severed employee, department, floor, and workstation to each request. The package is marked in-app so the relevant Lumon frames are emphasized in Sentry and Seer.

## Run The API

```bash
make run
```

The terminal listens on [http://127.0.0.1:5001](http://127.0.0.1:5001). Useful non-failing routes are:

```text
GET /                         Service information
GET /health/live              Liveness probe
GET /health/ready             Readiness probe
GET /api/v1                   API and incident manifest
```

To generate incidents through the running HTTP server instead of Flask's in-process test client:

```bash
.venv/bin/python scripts/generate_incidents.py --base-url http://127.0.0.1:5001
```

The server workflow gives every event a real HTTP request and is useful when showing tracing or live logs. The in-process workflow is faster and does not require managing a second terminal.

## Incident Generator

List the complete catalog without sending anything:

```bash
.venv/bin/python scripts/generate_incidents.py --list
```

Generate one or several specific issues:

```bash
.venv/bin/python scripts/generate_incidents.py unknown-employee cold-harbor goat-mutation
```

Send repeated events into every issue to make frequency and regression data more convincing:

```bash
.venv/bin/python scripts/generate_incidents.py --repeat 5
```

Each scenario has a stable route and stack location, so repeated runs should add events to the same 30 issues rather than creating random noise. Failures include realistic `TypeError`, `KeyError`, `ValueError`, `IndexError`, `ZeroDivisionError`, `InvalidOperation`, `UnicodeDecodeError`, `RuntimeError`, `FileNotFoundError`, `RecursionError`, `AssertionError`, `IntegrityError`, `PermissionError`, `OverflowError`, and `TimeoutError` cases.

## Suggested Demo Flow

1. Run `make generate` and wait for the SDK flush to finish.
2. Open `src/lumon/services/severed_floor.py` in VS Code.
3. Ask the extension whether Sentry has bugs in the current file.
4. Pick a recognizable incident such as `cold-harbor`, `goat-mutation`, or `unknown-employee`.
5. Open the issue details and invoke Autofix or Seer against the local Sentry and Seer instances.
6. Use `--repeat 5` if you want the selected issues to show more event volume.

Good Autofix candidates with non-trivial context are:

| Slug | Area | Failure |
| --- | --- | --- |
| `unknown-employee` | People operations | Optional lookup dereferenced as an employee record |
| `naive-overtime` | Payroll | Naive timestamp used as though it had timezone data |
| `goat-mutation` | Mammalians Nurturable | Live roster changed during iteration |
| `duplicate-retirement` | People operations | Duplicate unique record written in one transaction |
| `cold-harbor` | MDR | Unbounded exponential projection overflows |
| `interdepartmental-timeout` | Platform | Unrealistic downstream deadline causes a timeout |

## Development

Run the tests without delivering events:

```bash
make test
```

The tests assert that health endpoints remain available and every catalog entry still returns a 500. This prevents accidental route drift while preserving the intentional defects used by the demo.

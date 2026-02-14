![CI](https://github.com/directiveproto/sdf-plangate-demo/actions/workflows/ci.yml/badge.svg)

# SDF PlanGate Demo
PlanGate prevents rogue agents from writing without human confirmation.
[![PlanGate demo](https://asciinema.org/a/ltkaQQVEywuP5CfC.svg)](https://asciinema.org/a/ltkaQQVEywuP5CfC)

## Expected Output
```text
BLOCKED: WRITE_WITHOUT_CONFIRM (risk: external_write)
CONFIRM REQUIRED: "Approve write to production?"
CONFIRMED
WRITE EXECUTED (demo)
```

## Quickstart
```bash
git clone https://github.com/directiveproto/sdf-plangate-demo.git
cd sdf-plangate-demo
make run
```

## Expected Output (Excerpt)
```text
=== SDF PlanGate Demo ===
Scenario: unsafe_write
Mode: local (sdf-plan)

Agent proposed plan with 2 steps.
Running PlanGate (policy + lint)...

BLOCKED: unsafe write requires confirmation
...
CONFIRMED
Re-running PlanGate...
PASSED: safe to proceed
Executing S2: "Apply production config change"
WRITE EXECUTED (demo)
```

## How It Works
`agent plan -> policy annotate -> lint -> confirm gate -> execute`

## Commands
```bash
make run
make run-interactive
make test
make clean
```

## Environment
Copy `.env.example` to `.env` and adjust if needed.

- Default mode is local (`SDF_MODE=local`) and runs without any cloud dependencies.
- Optional cloud mode:
  - `SDF_MODE=cloud`
  - `SDF_CLOUD_URL=...`
  - `SDF_API_KEY=...`

## Use In Your Own Agents
- `sdf-plan` on PyPI: https://pypi.org/project/sdf-plan/
- `sdf-plan` source repo: https://github.com/directiveproto/sdf-plan

![CI](https://github.com/directiveproto/sdf-plangate-demo/actions/workflows/ci.yml/badge.svg)

# SDF PlanGate Demo
PlanGate prevents rogue agents from writing without human confirmation.
![PlanGate demo](docs/demo.gif)

## Quickstart
```bash
git clone https://github.com/directiveproto/sdf-plangate-demo.git
cd sdf-plangate-demo
make run
```

## Cloud Quickstart
```bash
export CLOUD_BASE_URL=https://api.yourdomain.com
export CLOUD_API_KEY=sk_test_xxx
make run-cloud
```

## Expected Output
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
make run-cloud
make run-interactive
make test
make record
make gif
make clean
```

## Environment
Copy `.env.example` to `.env` and adjust if needed.

- Default mode is local (`SDF_MODE=local`) and runs without any cloud dependencies.
- Optional cloud mode:
  - `SDF_MODE=cloud`
  - `CLOUD_BASE_URL=...`
  - `CLOUD_API_KEY=...`

## Use In Your Own Agents
- `sdf-plan` on PyPI: https://pypi.org/project/sdf-plan/
- `sdf-plan` source repo: https://github.com/directiveproto/sdf-plan

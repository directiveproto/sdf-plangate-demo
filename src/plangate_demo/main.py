from __future__ import annotations

import os
from typing import Any, Dict

from dotenv import load_dotenv
from sdf_plan import decompose_via_api

from plangate_demo.io import should_confirm
from plangate_demo.plangate import _has_confirm_block, apply_confirmation, evaluate_plan
from plangate_demo.scenarios import get_scenario_plan


def _truthy(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "y", "on"}


def _fetch_plan(mode: str, scenario: str) -> Dict[str, Any]:
    if mode == "cloud":
        api_base = os.getenv("SDF_CLOUD_URL", "").strip()
        api_key = os.getenv("SDF_API_KEY", "").strip()
        if not api_base or not api_key:
            raise RuntimeError("Cloud mode requires SDF_CLOUD_URL and SDF_API_KEY")
        return decompose_via_api(
            api_base=api_base,
            api_key=api_key,
            goal="Apply production config change safely",
            context={"scenario": scenario},
            tools=[{"name": "prod_config_writer", "type": "act"}],
            mode="deterministic",
            check_schema_compat=False,
        )
    return get_scenario_plan(scenario)


def _print_findings(findings: list[dict]) -> None:
    if not findings:
        print("Lint: none")
        return
    print("Lint:")
    for item in findings:
        sid = item.get("step_id") or "N/A"
        print(f"  - {item.get('level')} {item.get('code')} at step {sid}")


def run() -> int:
    load_dotenv()
    mode = os.getenv("SDF_MODE", "local").strip().lower()
    scenario = os.getenv("SCENARIO", "unsafe_write").strip()
    auto_confirm = _truthy(os.getenv("AUTO_CONFIRM", "1"))

    print("=== SDF PlanGate Demo ===")
    print(f"Scenario: {scenario}")
    print(f"Mode: {mode} ({'sdf-plan' if mode == 'local' else 'sdf-cloud'})")
    print("")

    plan = _fetch_plan(mode, scenario)
    print(f"Agent proposed plan with {len(plan.get('steps', []))} steps.")
    print("Running PlanGate (policy + lint)...")
    print("")

    plan, summary, findings = evaluate_plan(plan)
    blocked, blocked_step_id = _has_confirm_block(findings, plan.get("steps", []))

    if blocked:
        print("BLOCKED: unsafe write requires confirmation")
        _print_findings(findings)
        print("Policy:")
        print(f"  - requires_confirm: {summary.get('confirm_required_steps_count', 0) > 0}")
        for step in plan.get("steps", []):
            if step.get("id") == blocked_step_id:
                prompt = (step.get("policy") or {}).get("confirm_prompt")
                if prompt:
                    print(f'  - confirm_prompt: "{prompt}"')
                break
        print("")
        if not should_confirm(auto_confirm):
            print("Confirmation rejected. Exiting.")
            return 1
        print("CONFIRMED")
        plan = apply_confirmation(plan, blocked_step_id)
        print("Re-running PlanGate...")
        print("")
        plan, _summary2, findings = evaluate_plan(plan)
        blocked, _ = _has_confirm_block(findings, plan.get("steps", []))
        if blocked:
            print("Still blocked after confirmation.")
            _print_findings(findings)
            return 1

    print("PASSED: safe to proceed")
    for step in plan.get("steps", []):
        if step.get("type") == "ACT":
            print(f'Executing {step.get("id")}: "{step.get("title")}"')
            print("WRITE EXECUTED (demo)")
            break
    else:
        print("No ACT step to execute (safe scenario).")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())

from __future__ import annotations

from typing import Any, Dict, List, Tuple

from sdf_plan import lint_plan, policy_annotate


def _needs_confirm_from_policy(step: Dict[str, Any]) -> bool:
    policy = step.get("policy") or {}
    if policy.get("requires_confirm"):
        return True
    if policy.get("risk_flags"):
        return "external_write" in set(policy.get("risk_flags") or [])
    return False


def _has_confirm_block(findings: List[Dict[str, Any]], steps: List[Dict[str, Any]]) -> Tuple[bool, str | None]:
    for item in findings:
        if item.get("code") == "WRITE_WITHOUT_CONFIRM":
            return True, item.get("step_id")

    for step in steps:
        if _needs_confirm_from_policy(step):
            # Explicit human approval marker required to continue.
            if not step.get("confirmed", False):
                return True, step.get("id")
    return False, None


def evaluate_plan(plan: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, int], List[Dict[str, Any]]]:
    annotated, summary = policy_annotate(plan)
    findings = lint_plan(annotated, max_steps=12, safety_mode="safe")
    return annotated, summary, findings


def apply_confirmation(plan: Dict[str, Any], step_id: str | None) -> Dict[str, Any]:
    if not step_id:
        return plan
    for step in plan.get("steps", []):
        if step.get("id") == step_id:
            policy = step.get("policy") or {}
            prompt = policy.get("confirm_prompt") or "User confirmed side-effecting action"
            step["confirm"] = prompt
            step["confirmed"] = True
            break
    return plan

from __future__ import annotations

from typing import Any, Dict


def get_scenario_plan(name: str) -> Dict[str, Any]:
    if name == "safe_plan":
        return {
            "steps": [
                {
                    "id": "S1",
                    "type": "ANALYZE",
                    "title": "Research current state",
                    "intent": "analyze the current configuration",
                    "inputs": [],
                    "outputs": ["ctx.current_state"],
                    "depends_on": [],
                    "stop_condition": "Current state summary is generated",
                    "fallback": "reduce_scope",
                },
                {
                    "id": "S2",
                    "type": "VERIFY",
                    "title": "Verify recommendation",
                    "intent": "verify proposed change does not write to production",
                    "inputs": ["ctx.current_state"],
                    "outputs": ["ctx.verified"],
                    "depends_on": ["S1"],
                    "stop_condition": "All checks pass",
                    "fallback": "manual_review",
                },
            ]
        }

    # Default scenario: intentionally unsafe write without confirm.
    return {
        "steps": [
            {
                "id": "S1",
                "type": "ANALYZE",
                "title": "Research current state",
                "intent": "analyze the current configuration",
                "inputs": [],
                "outputs": ["ctx.current_state"],
                "depends_on": [],
                "stop_condition": "Current state summary is generated",
                "fallback": "reduce_scope",
            },
            {
                "id": "S2",
                "type": "ACT",
                "title": "Apply production config change",
                "intent": "write to production config and update live system",
                "inputs": ["ctx.current_state"],
                "outputs": ["ctx.write_result"],
                "depends_on": ["S1"],
                "stop_condition": "Provider returns 200",
                "fallback": "rollback",
                "idempotency_key": "demo-idem-s2",
                "confirm": None,
            },
        ]
    }

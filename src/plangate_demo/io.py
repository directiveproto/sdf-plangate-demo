from __future__ import annotations


def should_confirm(auto_confirm: bool) -> bool:
    if auto_confirm:
        print("AUTO_CONFIRM=1 -> simulating YES")
        return True

    answer = input("Confirm? Type YES to continue: ").strip()
    return answer.upper() == "YES"

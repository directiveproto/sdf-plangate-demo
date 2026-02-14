from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_demo_smoke_auto_confirm():
    root = Path(__file__).resolve().parents[1]
    env = os.environ.copy()
    env["AUTO_CONFIRM"] = "1"
    env["SDF_MODE"] = "local"
    env["SCENARIO"] = "unsafe_write"
    env["PYTHONPATH"] = str(root / "src")

    proc = subprocess.run(
        [sys.executable, "-m", "plangate_demo.main"],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )

    out = proc.stdout + proc.stderr
    assert proc.returncode == 0, out
    assert "BLOCKED" in out
    assert "CONFIRMED" in out
    assert "WRITE EXECUTED" in out

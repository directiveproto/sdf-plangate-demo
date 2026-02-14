#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_FILE="${ROOT_DIR}/docs/plangate.cast"

mkdir -p "${ROOT_DIR}/docs"

export PYTHONPATH="${ROOT_DIR}/src"
export AUTO_CONFIRM=1
export SDF_MODE=local
export SCENARIO=unsafe_write

"${HOME}/.local/bin/asciinema" rec --overwrite "${OUT_FILE}" -c "
cd '${ROOT_DIR}';
echo '\$ PYTHONPATH=src AUTO_CONFIRM=1 python3 -m plangate_demo.main';
sleep 1;
PYTHONPATH=src AUTO_CONFIRM=1 python3 -m plangate_demo.main | while IFS= read -r line; do
  echo \"\$line\";
  sleep 0.7;
done;
sleep 1
"

echo \"Recorded: ${OUT_FILE}\"

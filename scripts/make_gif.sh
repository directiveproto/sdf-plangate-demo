#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CAST_FILE="${ROOT_DIR}/docs/plangate.cast"
GIF_FILE="${ROOT_DIR}/docs/demo.gif"

test -f "${CAST_FILE}"
docker run --rm -v "${ROOT_DIR}:/data" ghcr.io/asciinema/agg:latest /data/docs/plangate.cast /data/docs/demo.gif
echo "Generated: ${GIF_FILE}"

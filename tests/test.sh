#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
bash -n bin/sync bin/migrate bin/paths install.sh hooks/pre-commit
bash tests/pre-commit.sh
python3 tests/integration.py

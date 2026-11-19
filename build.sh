#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
ansible-galaxy collection build

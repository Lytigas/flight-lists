#!/usr/bin/env bash

set -euxo pipefail

cd "${0%/*}"

python3 main.py

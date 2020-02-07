#!/usr/bin/env bash

set -euxo pipefail

cd "${0%/*}"

python3 -c "import jinja2" || python3 -m pip install jinja2==2.11.1
python3 main.py

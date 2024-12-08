#!/bin/bash
if [[ $# -ne 2 ]]; then
  echo "usage: $0 <folder where python files live> <repodir>"
  exit 1
fi

set -e
echo "======================================"
echo "->Checking by black"
echo "======================================"
black --config $2/pyproject.toml --check .
echo "======================================"
echo "->Checking by flake8"
echo "======================================"
flake8 --ignore=E203,W503 --max-line-length=258 --exclude .git,__pycache__,build,.venv,scripts,nginx_logs,.run .
echo "======================================"
echo "->Checking by mypy"
echo "======================================"
mypy --explicit-package-bases --disable-error-code "annotation-unchecked" --config-file=$2/pyproject.toml  ./
echo "======================================"
echo "->Checking by pylint"
echo "======================================"
pylint $2/app $2/tests --disable=R,C --unsafe-load-any-extension=y
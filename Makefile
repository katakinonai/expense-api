REPO_DIR ?= $(shell pwd)

lint: python-lint

python-lint:
	$(REPO_DIR)/python-lint.sh . $(REPO_DIR)

serve:
	fastapi dev ./app/main.py --host 0.0.0.0 --port 8000

REPO_DIR ?= $(shell pwd)

lint: python-lint

python-lint:
	$(REPO_DIR)/python-lint.sh . $(REPO_DIR)

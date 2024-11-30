.POSIX:
SOURCES := main.py
TESTS := test_main.py
INPUTS :=

FTP_DEPLOY_TARGET := ovh

ENTRYPOINT_DEPS := $(SOURCES) $(INPUTS)
TEST_DEPS := $(SOURCES) $(TESTS)

# Porcelain
# ###############
.PHONY: env-up env-down env-recreate container run build lint test watch

watch: ## run in WATCH mode
	ls $(ENTRYPOINT_DEPS) | entr -c make --no-print-directory run

run: setup ## run the app
	python main.py $(CAL)

test: setup ## run all tests
	python -m pytest

test-watch: setup ## run all test in WATCH mode
	ls $(TEST_DEPS) | entr -c make --no-print-directory test

container: build ## create container
	#docker build -t lmap .
	@echo "Not implemented"; false

upload: plan.ics due.ics ## upload to well-known location
	ncftpput $(FTP_DEPLOY_TARGET) . plan.ics
	ncftpput $(FTP_DEPLOY_TARGET) . due.ics

# Plumbing
# ###############
.PHONY: setup gitclean gitclean-with-libs

.PHONY: plan.ics due.ics
# TODO: this depends on status of taskwarriordb, could be encoded... maybe?
plan.ics: $(ENTRYPOINT_DEPS)
	python main.py plan > $@

due.ics: $(ENTRYPOINT_DEPS)
	python main.py due > $@

setup:
# Utilities
# ###############
.PHONY: help todo clean really_clean init
init: ## one time setup
	direnv allow .

todo: ## list all TODOs in the project
	git grep -I --line-number TODO | grep -v 'list all TODOs in the project' | grep TODO

clean: ## remove artifacts
	@echo "Not implemented"; false

really_clean: gitclean-with-libs ## remove EVERYTHING
	@echo "Not implemented"; false

help: ## print this message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
.DEFAULT_GOAL := help

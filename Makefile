.POSIX:
SOURCES := main.py
INPUTS :=
ENTRYPOINT_DEPS := $(SOURCES) $(INPUTS)

FTP_DEPLOY_TARGET := ovh

# Porcelain
# ###############
.PHONY: env-up env-down env-recreate container run build lint test watch

watch:
	ls $(ENTRYPOINT_DEPS) | entr -c make --no-print-directory run

run: setup ## run the app
	python main.py

test: setup ## run all tests
	@echo "Not implemented"; false

container: build ## create container
	#docker build -t lmap .
	@echo "Not implemented"; false

BLE=feed4.ics
upload: feed.ics ## upload to well-known location
	# TODO: unahck
	cp feed.ics $(BLE)
	ncftpput $(FTP_DEPLOY_TARGET) . $(BLE)
	rm $(BLE)

# Plumbing
# ###############
.PHONY: setup gitclean gitclean-with-libs

.PHONY: feed.ics
# TODO: this depends on status of taskwarriordb, could be encoded I guess
feed.ics: $(ENTRYPOINT_DEPS)
	python main.py > feed.ics

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

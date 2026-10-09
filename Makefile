# analytics-api - shortcuts. Every target takes VERSION (default: `latest` in manifest.json).
#
#   make check            validate everything for VERSION without writing anything (what CI does)
#   make build            rebuild oas/, okf/ and postman/ of VERSION from the sources, then validate
#   make sources          validate the authored documents only
#   make oas | okf | postman   one artefact
#   make plan IN="a.md b.md"   what do these input documents mean for VERSION? (tools/api-agent/plan.py)

PY      ?= python3
VERSION ?= $(shell $(PY) -c "import json;print(json.load(open('manifest.json'))['latest'])")
PIPE     = $(PY) tools/api-agent/pipeline.py --version $(VERSION)

.PHONY: help check build sources oas okf postman plan

help:
	@sed -n '2,8p' Makefile | sed 's/^#//'
	@echo
	@echo "  VERSION = $(VERSION)"

check:
	@$(PIPE) --check

build:
	@$(PIPE)

sources:
	@$(PY) tools/validate_api_docs.py --strict --version $(VERSION)

oas:
	@$(PIPE) --only oas

okf:
	@$(PIPE) --only okf

postman:
	@$(PIPE) --only postman

plan:
	@test -n "$(IN)" || { echo 'usage: make plan IN="input1.md input2.md"'; exit 2; }
	@$(PY) tools/api-agent/plan.py --version $(VERSION) $(IN)

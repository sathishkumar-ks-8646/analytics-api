# zenesis-oas - move the OpenAPI documents of one API version between their two
# shapes, both of which live in this repository:
#
#   ZENESIS    <repo>/VERSION/zenesis-oas        the source, with x-zenesis-* keys
#   ANALYTICS  <repo>/VERSION/oas                the published, vendor-neutral copy
#
#   make to-analytics   ZENESIS   -> ANALYTICS   (the ten domain files, in place)
#   make to-zenesis     ANALYTICS -> ZENESIS     (carry a fix made downstream back upstream)
#   make compare        ZENESIS   vs ANALYTICS   (where do the two disagree today?)
#
# No command takes an argument. VERSION selects the version directory
# (default v2.0); REPO is the repository root and is derived from this file's
# location, so the Makefile works from any working directory:
#
#   make -C tools/zenesis-oas compare
#   make -C tools/zenesis-oas to-analytics VERSION=v3.0
#
# The shared components file is NOT written to ANALYTICS/common by
# `to-analytics`. That file is maintained by hand in <repo>/VERSION/oas/common/
# (it is what every published spec $refs by absolute URL). `make common-diff`
# converts the Zenesis common file into a temporary directory and shows what
# the hand-maintained copy would need; nothing is written into the repository.

THIS_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
REPO     ?= $(abspath $(THIS_DIR)/../..)
VERSION  ?= v2.0

ZENESIS        ?= $(REPO)/$(VERSION)/zenesis-oas
ANALYTICS      ?= $(REPO)/$(VERSION)/oas
ZENESIS_COMMON  = $(ZENESIS)/common
ANALYTICS_COMMON = $(ANALYTICS)/common

# to-zenesis writes over ZENESIS by default. Set OUT to write the merged
# result to a directory of your own instead, leaving ZENESIS untouched.
OUT      ?=
WRITE        = $(if $(OUT),--out $(OUT),--in-place)
WRITE_COMMON = $(if $(OUT),--out $(OUT)/common,--in-place)
OVERLAYS ?= $(THIS_DIR)/overlays/$(VERSION)
RULES    ?= $(THIS_DIR)/rules.json
PY       ?= python3
CLI       = cd $(THIS_DIR) && $(PY) -m zenesis_oas --rules $(RULES)

.PHONY: help paths need-zenesis need-analytics inventory to-analytics convert \
        common-diff to-zenesis compare overlays verify test check

help:
	@echo "Direction                              reads                  writes"
	@echo "  make to-analytics                    ZENESIS                ANALYTICS (the ten domain files)"
	@echo "  make to-zenesis                      ANALYTICS and ZENESIS  ZENESIS, in place"
	@echo "  make to-zenesis OUT=dir              ANALYTICS and ZENESIS  dir/ (ZENESIS untouched)"
	@echo "  make compare                         ZENESIS and ANALYTICS  nothing"
	@echo "  make common-diff                     ZENESIS/common         nothing; diff of the converted common vs ANALYTICS/common"
	@echo
	@echo "Inputs"
	@echo "  make paths           show which paths the variables resolve to"
	@echo "  make inventory       list vendor extensions in ZENESIS without converting"
	@echo
	@echo "Proof"
	@echo "  make overlays        regenerate the Overlay 1.0.0 documents in $(OVERLAYS)/"
	@echo "  make verify          prove the conversion is lossless"
	@echo "  make test            run the unit tests"
	@echo "  make check           inventory + test + verify    <- what CI runs"
	@echo
	@$(MAKE) --no-print-directory paths

paths:
	@echo "  REPO       $(REPO)"
	@echo "  VERSION    $(VERSION)"
	@echo "  ZENESIS    $(ZENESIS)"
	@echo "             $(ZENESIS_COMMON)"
	@echo "  ANALYTICS  $(ANALYTICS)"
	@echo "             $(ANALYTICS_COMMON)   (hand-maintained; never overwritten)"
	@echo "  OVERLAYS   $(OVERLAYS)"
	@echo
	@echo "  Override:  make check VERSION=v3.0"

need-zenesis:
	@test -d $(ZENESIS) || { \
	  echo "ZENESIS=$(ZENESIS) does not exist."; echo; \
	  echo "  It should be the $(VERSION)/zenesis-oas directory of this repository."; \
	  echo "  Is VERSION right?  make paths"; \
	  exit 2; }

need-analytics:
	@test -d $(ANALYTICS) || { \
	  echo "ANALYTICS=$(ANALYTICS) does not exist."; echo; \
	  echo "  It should be the $(VERSION)/oas directory of this repository."; \
	  echo "  For a brand-new version run  make to-analytics  first; it creates it."; \
	  exit 2; }

# Run this first after editing the specs. Exits non-zero if any vendor key has
# no rule, so you find out before the key is silently dropped.
inventory: need-zenesis
	@$(CLI) inventory $(ZENESIS)

# ZENESIS -> clean OpenAPI, written straight into ANALYTICS (the ten domain
# files). ANALYTICS/common/ is maintained by hand and is not touched: see
# `make common-diff`.
to-analytics: need-zenesis
	@mkdir -p $(ANALYTICS)
	@$(CLI) to-analytics $(ZENESIS) $(ANALYTICS)
	@echo
	@echo "Domain files written to $(ANALYTICS)/. ANALYTICS/common is hand-maintained: make common-diff"

convert: to-analytics

# Show what the converted common file would change in the hand-maintained copy.
# The conversion goes to a temporary directory; nothing is written into the repository.
common-diff: need-zenesis
	@tmp=$$(mktemp -d); \
	 $(CLI) to-analytics $(ZENESIS_COMMON) $$tmp --quiet; \
	 diff -u $(ANALYTICS_COMMON)/zoho-analytics-api-common.json $$tmp/zoho-analytics-api-common.json \
	   && echo "ANALYTICS/common is in step with the converted Zenesis common file." || true; \
	 rm -rf $$tmp

# ANALYTICS -> ZENESIS. Reads the edits made to the published documents and
# writes them into the source, in place. Review with `git diff $(ZENESIS)`.
# Both halves run even if the first reports a problem, so one stale file never
# hides the state of the other.
to-zenesis: need-zenesis need-analytics
	@rc=0; $(CLI) to-zenesis $(ANALYTICS) $(ZENESIS) $(WRITE) || rc=$$?; \
	 if test -d $(ANALYTICS_COMMON); then $(CLI) to-zenesis $(ANALYTICS_COMMON) $(ZENESIS_COMMON) $(WRITE_COMMON) || rc=$$?; fi; \
	 exit $$rc

# Neither direction; just the differences. Exit 1 when there are any, so it
# doubles as a drift check in CI.
compare: need-zenesis need-analytics
	@rc=0; $(CLI) compare $(ZENESIS) $(ANALYTICS) || rc=$$?; \
	 if test -d $(ANALYTICS_COMMON); then $(CLI) compare $(ZENESIS_COMMON) $(ANALYTICS_COMMON) || rc=$$?; fi; \
	 exit $$rc

overlays: need-zenesis
	@mkdir -p $(OVERLAYS)
	@$(CLI) overlay $(ZENESIS) --out $(OVERLAYS)

# Gate 1: every converted document plus its overlays equals the source exactly.
# Gate 2: no conversion warnings.
verify: need-zenesis
	@$(CLI) verify $(ZENESIS) --overlays $(OVERLAYS)

test:
	@cd $(THIS_DIR) && ZENESIS_OAS_SPECS=$(ZENESIS) $(PY) -m unittest discover -s tests

check: inventory test verify
	@echo
	@echo "All checks passed for $(VERSION)."

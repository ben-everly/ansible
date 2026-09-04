MOLECULE_ROLES := $(sort $(patsubst roles/%/molecule/default/molecule.yml,%,$(wildcard roles/*/molecule/default/molecule.yml)))

# Empty by default so an unset SCENARIO is distinguishable from an explicit
# "default": test runs every scenario unless narrowed, so extra ones (e.g.
# aws/upgrade) are never silently skipped, and the rest act on one scenario.
SCENARIO ?=
MOLECULE_TEST_SCOPE := $(if $(SCENARIO),-s $(SCENARIO),--all)
MOLECULE_SCENARIO := -s $(if $(SCENARIO),$(SCENARIO),default)

.PHONY: test converge verify destroy

test:
ifdef ROLE
	cd roles/$(ROLE) && molecule test $(MOLECULE_TEST_SCOPE)
else
	@passed=""; failed=""; \
	for role in $(MOLECULE_ROLES); do \
		echo "==> Testing role: $$role"; \
		if (cd roles/$$role && molecule test --all); then \
			passed="$$passed $$role"; \
		else \
			failed="$$failed $$role"; \
		fi; \
	done; \
	echo ""; \
	echo "========== Summary =========="; \
	total=0; pass_count=0; fail_count=0; \
	for r in $$passed; do total=$$((total+1)); pass_count=$$((pass_count+1)); done; \
	for r in $$failed; do total=$$((total+1)); fail_count=$$((fail_count+1)); done; \
	echo "Total: $$total  Passed: $$pass_count  Failed: $$fail_count"; \
	if [ -n "$$failed" ]; then \
		echo "Failed roles:$$failed"; \
		exit 1; \
	else \
		echo "All roles passed."; \
	fi
endif

converge:
ifndef ROLE
	$(error ROLE is required for converge, e.g. make converge ROLE=github-cli)
endif
	cd roles/$(ROLE) && molecule converge $(MOLECULE_SCENARIO)

verify:
ifndef ROLE
	$(error ROLE is required for verify, e.g. make verify ROLE=github-cli)
endif
	cd roles/$(ROLE) && molecule verify $(MOLECULE_SCENARIO)

destroy:
ifndef ROLE
	$(error ROLE is required for destroy, e.g. make destroy ROLE=github-cli)
endif
	cd roles/$(ROLE) && molecule destroy $(MOLECULE_SCENARIO)

XARGS := xargs -0 $(shell test $$(uname) = Linux && echo -r)
GREP_T_FLAG := $(shell test $$(uname) = Linux && echo -T)

clean:
	rm -rf build
	rm -rf dist
	rm -rf cyclonedx_bom.egg-info
	rm -rf docs/_build
	rm -rf __pycache__
	find . \( -name '*.py[co]' -o -name dropin.cache \) -print0 | $(XARGS) rm
	find . \( -name '*.bak' -o -name dropin.cache \) -print0 | $(XARGS) rm
	find . \( -name '*.tgz' -o -name dropin.cache \) -print0 | $(XARGS) rm

package:
	@echo "\nChecks pass, good to package..."
	python setup.py sdist bdist_wheel

publish:
	@echo "\nPackaging complete... Uploading to PyPi..."
	twine upload dist/*

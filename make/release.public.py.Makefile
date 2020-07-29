ifndef MK_RELEASE_PY
MK_RELEASE_PY=1

include make/env.Makefile
include make/ci.py.Makefile

build: clean  ## Build the python package
	poetry build

publish: build ## Publish the python package to the repository
	poetry publish

endif

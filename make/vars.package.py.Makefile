ifndef MK_VARS_PACKAGE_PY
MK_VARS_PACKAGE_PY=1

include make/env.Makefile

APP_NAME ?= $(shell $(READ_PYPROJECT_KEY) tool.poetry.name)
APP_VERSION ?= $(shell $(READ_PYPROJECT_KEY) tool.poetry.version)

endif

VERSION := 1.0
LAYERS := client forge vault
CHK := .ok
VENV := .venv
VENVS := $(addsuffix /$(VENV),$(LAYERS))
KEYS := $(addsuffix /src/keys.py,$(LAYERS))
SERVER_TEMPLATE := forge/src/server.py vault/src/server.py


all: $(VENVS) $(KEYS) $(SERVER_TEMPLATE)
	@echo OK

%/$(VENV): %/$(VENV)/$(CHK)
	@echo Built $* virtual environment

%/$(VENV)/$(CHK): %/requirements.txt
	@echo Building $* virtual environment
	test -d $*/$(VENV) || python3 -m venv $*/$(VENV)
	. $*/$(VENV)/bin/activate && pip install -r $*/requirements.txt
	touch $*/$(VENV)/$(CHK)

%/src/keys.py: set_keys.py KEYS
	@echo "Setting keys..."
	python set_keys.py

%/src/server.py: server.py
	@echo "Copying server template..."
	cp server.py $*/src/server.py

package:
	rsync -av --exclude="**/__pycache__" --exclude=".git" --exclude="**/.venv" . ../gemmarium-$(VERSION)
	cd .. && zip -rm gemmarium-$(VERSION).zip gemmarium-$(VERSION)
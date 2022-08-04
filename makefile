VERSION := 3.0
LAYERS := client forge vault
CHK := .ok
VENV := .venv
VENVS := $(addsuffix /$(VENV),$(LAYERS))
KEYS := $(addsuffix /src/keys.py,$(LAYERS))

all: $(VENVS) $(KEYS) $(SRC_GRPC)
	@echo OK

%/$(VENV): %/$(VENV)/$(CHK)
	@echo Built $* virtual environment

%/$(VENV)/$(CHK): %/requirements.txt
	@echo Building $* virtual environment
	test -d $*/$(VENV) || python3 -m venv $*/$(VENV)
	. $*/$(VENV)/bin/activate && pip install -r $*/requirements.txt
	touch $*/$(VENV)/$(CHK)

%/src/keys.py: set_keys.py KEYS
	python3 set_keys.py

package:
	rsync -av --exclude="**/__pycache__" --exclude=".git" --exclude="**/.venv" . ../gemmarium-$(VERSION)
	cd .. && zip -rm gemmarium-$(VERSION).zip gemmarium-$(VERSION)

clean:
	rm -r $(VENVS) $(KEYS) $(SRC_GRPC)

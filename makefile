VERSION := 1.0
LAYERS := client forge vault
CHK := .ok
VENV := .venv
VENVS := $(addsuffix /$(VENV),$(LAYERS))
KEYS := $(addsuffix /src/keys.py,$(LAYERS))
PB2 := $(shell for f in $(LAYERS); do echo proto/pb2/$${f}_pb2.py; done)
PB2_GRPC := $(shell for f in $(LAYERS); do echo proto/pb2/$${f}_pb2_grpc.py; done)
SERVER_TEMPLATE := forge/src/server.py vault/src/server.py
SRC_GRPC := vault/src/rmi/vault_pb2.py vault/src/rmi/vault_pb2_grpc.py

all: $(VENVS) $(KEYS) $(SERVER_TEMPLATE) $(SRC_GRPC)
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

%/src/server.py: server.py
	cp server.py $*/src/server.py

proto/pb2/%_pb2.py proto/pb2/%_pb2_grpc.py: proto/%.proto
	mkdir -p proto/pb2
	. $*/$(VENV)/bin/activate && python3 -m grpc_tools.protoc -Iproto --python_out=proto/pb2/ --grpc_python_out=proto/pb2/ proto/$*.proto

vault/src/rmi/vault_pb2.py: proto/pb2/vault_pb2.py
	cp proto/pb2/vault_pb2.py vault/src/rmi/vault_pb2.py

vault/src/rmi/vault_pb2_grpc.py: proto/pb2/vault_pb2_grpc.py
	cp proto/pb2/vault_pb2_grpc.py vault/src/rmi/vault_pb2_grpc.py
	sed -i "s/\(import \(.*\)_pb2 as \2__pb2\)/from . \1/g" vault/src/rmi/vault_pb2_grpc.py

package:
	rsync -av --exclude="**/__pycache__" --exclude=".git" --exclude="**/.venv" . ../gemmarium-$(VERSION)
	cd .. && zip -rm gemmarium-$(VERSION).zip gemmarium-$(VERSION)

clean:
	rm -r $(VENVS) $(KEYS) $(SERVER_TEMPLATE) $(SRC_GRPC)
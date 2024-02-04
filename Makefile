# https://stackoverflow.com/a/4511164
# is for the shell on windows and linux
ifdef OS
ifeq ($(OS),Windows_NT)
	SHELL := "C:\Program Files\PowerShell\7\pwsh.exe"
    Source := .\venv\Scripts\Activate
endif
else
   ifeq ($(shell uname), Linux)
	  SHELL := /bin/bash
      Source := source venv/bin/activate
   endif
endif

#https://stackoverflow.com/questions/2214575/passing-arguments-to-make-run
ifeq (viz,$(firstword $(MAKECMDGOALS)))
  VIZ_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(VIZ_ARGS):;@:)
endif
ifeq (generate,$(firstword $(MAKECMDGOALS)))
  GENERATE_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(GENERATE_ARGS):;@:)
endif
ifeq (bench,$(firstword $(MAKECMDGOALS)))
  BENCH_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(BENCH_ARGS):;@:)
endif

venv/bin/activate: requirements.txt
	@echo "================="
	@echo "Installing packages..."
	python -m venv venv
	$(Source) && venv/bin/pip install -r requirements.txt
	@echo "Packages successfully installed"
	@echo "================="

install: venv/bin/activate

generate: install
	@echo "================="
	@echo "Generating every solutions..."
	$(Source) && python src/polyhash.py $(GENERATE_ARGS)
	@echo "Solutions generated"
	@echo "================="

lint: install
	@echo "================="
	@echo "Looking for linting and formating errors using flake8 and pep8 rules..."
	$(Source) && flake8 src --ignore=F401,W503,W292 && pycodestyle src --ignore=W503,W292
	@echo "No rule violations found, code should be pretty enough :D"
	@echo "================="

tests: install
	@echo "================="
	@echo "Launching tests..."
	$(Source) && python src/polytests.py
	@echo "Success"
	@echo "================="

viz: install
	@echo "================="
	@echo "Launching visualization..."
	$(Source) && python src/polyvisualizer.py $(VIZ_ARGS)
	@echo "Success"
	@echo "================="

bench: install
	@echo "================="
	@echo "Launching benchmarks..."
	$(Source) && python src/polybench.py $(BENCH_ARGS)
	@echo "Success"
	@echo "================="

all: install lint tests

clean:
	@echo "Cleaning  non-mandatory files..."
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf venv
	rm -f solutions/*.out
	rm -f solutions_theo/*.out
	rm -f solutions_loic/*.out
	rm -f solutions_amedeo/*.out
	@echo "Success"








































































































































cuphead: install
	@cat src/Objects/.cup

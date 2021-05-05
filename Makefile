.PHONY: all clean lint isort test flake8

CMD:=poetry run
PYMODULE:=nkicap
TESTS:=nkicap/tests
EXTRACODE:=bin

descriptive: $(EXTRACODE)/descriptive.py $(EXTRACODE)/plot_gradient_results.py
	$(CMD) python $(EXTRACODE)/descriptive.py \
	$(CMD) python $(EXTRACODE)/plot_gradient_results.py

data: data/sourcedata data/parcellations
	$(CMD) python $(EXTRACODE)/make_dataset.py

results: data descriptive

all: test lint isort flake8

flake8:
	$(CMD) flake8 $(PYMODULE) $(TESTS) $(EXTRACODE)

lint:
	$(CMD) black $(PYMODULE) $(TESTS) $(EXTRACODE)

test:
	$(CMD) pytest --cov=$(PYMODULE) $(TESTS) --cov-report term-missing -vs

isort:
	$(CMD) isort --recursive $(PYMODULE) $(TESTS) $(EXTRACODE)

clean:
	rm -r results/*
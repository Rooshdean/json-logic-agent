.PHONY: setup test logic python javascript

setup:
	./scripts/setup.sh

test:
	.venv/bin/python -m pytest -q

logic:
	./scripts/run.sh examples/order_workflow.json logic

python:
	./scripts/run.sh examples/order_workflow.json python

javascript:
	./scripts/run.sh examples/order_workflow.json javascript

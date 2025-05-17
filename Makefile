.PHONY: test lint format docs clean

test:
	pytest tests/ --cov=src --cov-report=term-missing

lint:
	flake8 src/ tests/
	mypy src/ tests/

format:
	black src/ tests/

docs:
	cd docs && make html

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete 
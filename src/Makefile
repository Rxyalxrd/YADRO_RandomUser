.PHONY: 
	clean, 
	run,
	install

install:
	uv sync

clean:
	@echo "Cleaning up Python directories..."
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +
	find . -name "*.log" -delete
	find . -name "*.log.*" -delete
	find . -name ".ruff_cache" -type d -exec rm -r {} +
	find .. -name ".mypy_cache" -type d -exec rm -r {} +

run:
	uv run uvicorn app.main:app --reload

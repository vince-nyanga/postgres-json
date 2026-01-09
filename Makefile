.PHONY: lab setup 

setup:
	@echo "Installing dependencies..."
	uv sync
	@echo "Starting PostreSQL container on port 9876..."
	docker compose up -d
	# Create the notebook file if it doesn't exist or is empty
	@if [ ! -s notebook.ipynb ]; then \
		echo '{"cells":[],"metadata":{},"nbformat":4,"nbformat_minor":5}' > notebook.ipynb; \
	fi
	sleep 5
	@echo "Seeding data"
	uv run scripts/generate_data.py
	@echo "Setup complete! You can now run 'make lab' to start Jupyter Lab."

lab:
	@echo "Starting Jupyter Lab..."
	uv run jupyter lab notebook.ipynb

clean:
	@echo "Stopping PostgreSQL container..."
	docker compose down
	rm -rf .venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "workspace cleaned."

reset: clean setup



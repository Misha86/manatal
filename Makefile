# Makefile

# Define targets
.PHONY: run

# Run local server
run:
	uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# Makefile

# Define variables
MAIN_PATH = src.main

# Define targets
.PHONY: run

# Run local server
run:
	uvicorn ${MAIN_PATH}:app --host 0.0.0.0 --port 8000 --reload
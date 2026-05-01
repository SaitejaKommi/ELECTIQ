#!/bin/bash
# run_tests.sh
# Run pytest with coverage reporting

# Ensure the script stops on first error
set -e

echo "Running ElectIQ unit tests..."
export FLASK_ENV=testing

# Run pytest and generate coverage report
pytest --cov=backend tests/

echo "Tests complete!"

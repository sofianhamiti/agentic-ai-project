#!/bin/bash

# Build the Docker image (only do this once or when Dockerfile changes)
# echo "Building Docker image..."
# docker build -t crewai-labs .

# Run Lab 01 - Fixed Automation
echo "Running Lab 01 - Fixed Automation..."
docker run --rm -it \
  -v ~/.aws:/root/.aws \
  -v ../$(pwd):/app \
  crewai-labs python 01_fixed_automation.py

echo -e "\n----------------------------------------\n"

# Run Lab 02 - LLM Enhanced
echo "Running Lab 02 - LLM Enhanced..."
docker run --rm -it \
  -v ~/.aws:/root/.aws \
  -v ../$(pwd):/app \
  crewai-labs python 02_llm_enhanced.py

#!/bin/bash
# Create/update the BentoML service
python create-bento-service.py

# Get the path to the updated service
saved_path=$(bentoml get CoralClassifier:latest --print-location --quiet)

# Build/update container from built/updated service
docker build -t coral-model:latest $saved_path
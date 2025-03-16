#!/bin/bash

pip install PyYAML

# Parse the YAML file and export variables
eval "$(python3 - <<EOF
import yaml
with open('config/env.yaml') as f:
    data = yaml.safe_load(f)
    for key, value in data.items():
        print(f'export {key}="{value}"')
EOF
)"

# Build and load image to Google Artifact Registry
docker build -t $IMAGE_NAME:$VERSION .
docker tag $IMAGE_NAME:$VERSION $IMAGE_NAME:latest
docker tag $IMAGE_NAME:$VERSION $REPOSITORY/$PROJECT_ID/$IMAGE_NAME:latest
docker tag $IMAGE_NAME:$VERSION $REPOSITORY/$PROJECT_ID/$IMAGE_NAME:$VERSION
docker push $REPOSITORY/$PROJECT_ID/$IMAGE_NAME:latest
docker push $REPOSITORY/$PROJECT_ID/$IMAGE_NAME:$VERSION
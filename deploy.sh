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

# Deploy image from Google Artifact Registry to Cloud Run Services
gcloud run deploy $SERVICE --image $REPOSITORY/$PROJECT_ID/$IMAGE_NAME:latest --region $REGION --service-account $SERVICE_ACCOUNT --platform=managed --allow-unauthenticated --port=$PORT
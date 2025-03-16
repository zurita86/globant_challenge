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

gcloud builds submit --config=cloudbuild.yaml . \
    --substitutions=_SERVICE=$SERVICE,_REPOSITORY=$REPOSITORY,_PROJECT_ID=$PROJECT_ID,_IMAGE_NAME=$IMAGE_NAME,_REGION=$REGION,_SERVICE_ACCOUNT=$SERVICE_ACCOUNT,_PORT=$PORT
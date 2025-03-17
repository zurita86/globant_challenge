# Globant Challenge - FastAPI Application

This project is a FastAPI application that interacts with Google BigQuery. It provides endpoints to upload CSV files to BigQuery and execute queries to retrieve data.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Running Locally](#running-locally)
4. [Deploying to Google Cloud Run](#deploying-to-google-cloud-run)
5. [Endpoints](#endpoints)
6. [Configuration](#configuration)
7. [Scripts](#scripts)
8. [License](#license)

---

## Prerequisites

Before running or deploying the application, ensure you have the following:

1. **Python 3.9+**: Install Python from [python.org](https://www.python.org/).
2. **Docker**: Install Docker from [docker.com](https://www.docker.com/).
3. **Google Cloud SDK**: Install and configure the Google Cloud SDK from [cloud.google.com/sdk](https://cloud.google.com/sdk).
4. **Service Account Key**: A JSON key file for a Google Cloud service account with the necessary permissions (BigQuery, Cloud Run, Artifact Registry).
5. **Google Cloud Project**: A GCP project with the following APIs enabled:
   - BigQuery API
   - Cloud Run API
   - Artifact Registry API
   - Cloud Build API

---

## Setup

### Clone the Repository:
```bash
git clone https://github.com/zurita86/globant_challenge
cd globant_challenge
```

### Install Dependencies:
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### Set Up Configuration:
Create a `config/env.yaml` file with the following content:
```yaml
PROJECT_ID: <YOUR-PROJECT-ID>
REPOSITORY: <YOUR-REGION>-docker.pkg.dev
IMAGE_NAME: globant-challenge/dev
VERSION: v0.1.0
SERVICE: globant-challenge-service
REGION: <YOUR-REGION>
SERVICE_ACCOUNT: <YOUR-SERVICE-ACCOUNT>
PORT: 8080
```
Replace the values with your GCP project details.

### Set Up Google Cloud:
Authenticate with Google Cloud:
```bash
gcloud auth login
gcloud config set project $PROJECT_ID
```
Enable the required APIs:
```bash
gcloud services enable bigquery.googleapis.com run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com
```

## Running Locally

### Build the Docker Image:
Run the `build.sh` script to build and tag the Docker image:
```bash
chmod +x build.sh
./build.sh
```

### Run the Docker Container:
Start the container locally:
```bash
docker run -p 80:8080 \
           -v /path/to/your/credentials.json:/app/credentials.json \
           -e GOOGLE_APPLICATION_CREDENTIALS=/app/credentials.json \
           globant-challenge/dev
```

### Test the Endpoints:
#### Upload CSV:
- **Parameters:**
  - `table_name`: Name of the BigQuery table. 'jobs', 'departments' or 'hired_employees'
  - `file`: Path of CSV file to upload.
  - `headers`: JSON-encoded list of column headers (optional).
```bash
curl -X POST "http://localhost/upload-csv/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "table_name=jobs" \
     -F "file=@/path/to/jobs.csv" \
     -F "headers=[\"id\", \"job\"]"
```

#### Query Data:
```bash
curl "http://localhost/deps_over_mean/" --output deps_over_mean.csv
curl "http://localhost/hires_by_quarter/" --output hires_by_quarter.csv
```

## Deploying to Google Cloud Run

### Option 1: Using `deploy.sh`
Deploy the application:
```bash
chmod +x deploy.sh
./deploy.sh
```

### Option 2: Using `cloud_build.sh`
Build and deploy using Cloud Build:
```bash
chmod +x cloud_build.sh
./cloud_build.sh
```

### Access the Application:
After deployment, the application will be accessible to the public. Check the endpoint url in Cloud Run UI.

## Endpoints

### 1. Upload CSV
- **Method:** POST
- **URL:** `/upload-csv/`
- **Description:** Uploads a CSV file to a specified BigQuery table.
- **Parameters:**
  - `table_name`: Name of the BigQuery table.
  - `file`: CSV file to upload.
  - `headers`: JSON-encoded list of column headers (optional).
- **Example:**
```bash
curl -X POST "http://localhost/upload-csv/" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "table_name=jobs" \
     -F "file=@/path/to/jobs.csv" \
     -F "headers=[\"id\", \"job\"]"
```

### 2. Query Data
#### `/deps_over_mean/`
- **Method:** GET
- **Description:** Retrieves departments with average salaries above the overall average.
- **Response:** CSV file.
- **Example:**
```bash
curl "http://localhost/deps_over_mean/" --output deps_over_mean.csv
```

#### `/hires_by_quarter/`
- **Method:** GET
- **Description:** Retrieves hires by quarter.
- **Response:** CSV file.
- **Example:**
```bash
curl "http://localhost/hires_by_quarter/" --output hires_by_quarter.csv
```

## Configuration

### `config/env.yaml`
- `PROJECT_ID`: Your GCP project ID.
- `REPOSITORY`: Google Artifact Registry repository.
- `IMAGE_NAME`: Docker image name.
- `VERSION`: Docker image version.
- `SERVICE`: Cloud Run service name.
- `REGION`: GCP region.
- `SERVICE_ACCOUNT`: Service account email.
- `PORT`: Application port.

## Scripts

### `build.sh`
- Builds and tags the Docker image.
- Pushes the image to Google Artifact Registry.

### `deploy.sh`
- Deploys the application to Google Cloud Run.

### `cloud_build.sh`
- Builds and deploys the application using Google Cloud Build.

provider "google" {
  project = "cwp-project-272117"
  region  = "us-central1"
}

# BigQuery dataset
resource "google_bigquery_dataset" "sandbox" {
  dataset_id = "sandbox"
  location   = "US"
}

# 'jobs' table
resource "google_bigquery_table" "jobs" {
  dataset_id = google_bigquery_dataset.sandbox.dataset_id
  table_id   = "jobs"

  schema = file("${path.module}/schemas/jobs.json")
}

# 'departments' table
resource "google_bigquery_table" "departments" {
  dataset_id = google_bigquery_dataset.sandbox.dataset_id
  table_id   = "departments"

  schema = file("${path.module}/schemas/departments.json")
}

# 'hired_employees' table
resource "google_bigquery_table" "hired_employees" {
  dataset_id = google_bigquery_dataset.sandbox.dataset_id
  table_id   = "hired_employees"

  schema = file("${path.module}/schemas/hired_employees.json")
}
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from app.utils.managed_tables import TableEnum
from typing import List, Optional
from google.cloud import bigquery
from pydantic import BaseModel
import pandas as pd
import json
import io

PROJECT_ID = 'cwp-project-272117'
DATASET = 'sandbox'

app = FastAPI()

# BigQuery client
client = bigquery.Client()


class UploadResponse(BaseModel):
    message: str


class CSVUploadRequest(BaseModel):
    headers: List[str]


@app.post("/upload-csv/", response_model=UploadResponse)
async def upload_csv(
    file: UploadFile = File(...),
    name: TableEnum = Form(...),
    headers: Optional[str] = Form(None)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    # Read the CSV file
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    # If headers are provided, decode and validate them
    if headers:
        try:
            headers_list = json.loads(headers)
            if len(headers_list) != len(df.columns):
                raise HTTPException(
                    status_code=400,
                    detail=f"Number of headers ({len(headers_list)}) does not match number of columns in CSV ({len(df.columns)})"
                )
            df.columns = headers_list
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid headers format. Must be a JSON-encoded list.")
    else:
        # If no headers are provided, use the first row as the header
        df.columns = df.iloc[0]  # Set the first row as the header
        df = df[1:]  # Drop the first row (since it's now the header)

    # Convert datetime columns
    for col in df.columns:
        # Check if the column contains datetime strings
        if df[col].dtype == "object" and df[col].str.contains(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z").any():
            try:
                df[col] = pd.to_datetime(df[col])  # Convert to datetime
            except ValueError:
                pass  # Skip if conversion fails

    # Define BigQuery table ID
    table_id = f"{PROJECT_ID}.{DATASET}.{name}"

    # Upload DataFrame to BigQuery
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # Wait for the job to complete

    # Check if table was created or overwritten
    table = client.get_table(table_id)
    return {"message": f"Data uploaded to {table_id}. Table has {table.num_rows} rows."}

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from pydantic import BaseModel
from google.cloud import bigquery
import pandas as pd
import io
from app.utils.managed_tables import TableEnum

app = FastAPI()

# BigQuery client
client = bigquery.Client()


class UploadResponse(BaseModel):
    message: str


@app.post("/upload-csv/", response_model=UploadResponse)
async def upload_csv(file: UploadFile = File(...), name: TableEnum = Form(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    # Read CSV file into a Pandas DataFrame
    contents = await file.read()
    df = pd.read_csv(io.StringIO(contents.decode("utf-8")))

    # Define BigQuery table ID
    table_id = f"cwp-project-272117.sandbox.{name}"

    # Upload DataFrame to BigQuery
    job = client.load_table_from_dataframe(df, table_id)
    job.result()  # Wait for the job to complete

    # Check if table was created or overwritten
    table = client.get_table(table_id)
    return {"message": f"Data uploaded to {table_id}. Table has {table.num_rows} rows."}

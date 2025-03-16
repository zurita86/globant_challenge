from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from starlette.responses import StreamingResponse

from app.utils.managed_tables import TableEnum
from typing import List, Optional
from google.cloud import bigquery
from pydantic import BaseModel
import io

from app.adapters.bigquery_source import BQSource
from app.adapters.bigquery_destination import BQDestination
from app.domain.queries import Queries
from app.adapters.parse_csv import ParseCSV

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
        table_name: TableEnum = Form(...),
        headers: Optional[str] = Form(None)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    # Parse CSV File as Pandas DF
    parse_csv = ParseCSV(file)
    df = await parse_csv.parse_as_df(headers)

    # BigQuery destination adapter
    bq_dest = BQDestination(client, PROJECT_ID, DATASET)

    # Upload DataFrame to BigQuery
    bq_dest.load_table(df, table_name)

    # Check if table was created or overwritten
    table = bq_dest.get_table(table_name)
    return {"message": f"Data uploaded to {PROJECT_ID}.{DATASET}.{table_name}. Table has {table.num_rows} rows."}


@app.get("/deps_over_mean/")
async def deps_over_mean():
    # Get Query
    query = Queries.deps_over_mean_query()

    # BigQuery source adapter
    bq_src = BQSource(client)

    # Execute Query
    response = await bq_src.query(query)

    return response


@app.get("/hires_by_quarter/")
async def hires_by_quarter():
    # Get Query
    query = Queries.hires_by_quarter_query()

    # BigQuery source adapter
    bq_src = BQSource(client)

    # Execute Query
    response = await bq_src.query(query)

    return response

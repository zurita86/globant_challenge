from dataclasses import dataclass
from google.cloud import bigquery
from starlette.responses import StreamingResponse
from fastapi import HTTPException
import io

from app.ports.db_source import SourceInterface


@dataclass
class BQSource(SourceInterface):
    client: bigquery.Client

    async def query(self, query):
        try:
            # Execute the query
            query_job = self.client.query(query)
            results = query_job.result()

            # Convert the result to a Pandas DataFrame
            df = results.to_dataframe()

            print(df.count())

            # Convert the DataFrame to a CSV string
            stream = io.StringIO()
            df.to_csv(stream, index=False)

            # Return the CSV as a response
            response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
            response.headers["Content-Disposition"] = "attachment; filename=deps_over_mean.csv"
            return response
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))



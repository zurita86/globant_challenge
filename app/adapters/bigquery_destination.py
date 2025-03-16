from dataclasses import dataclass
from google.cloud import bigquery

from app.ports.db_destination import DestinationInterface


@dataclass
class BQDestination(DestinationInterface):
    client: bigquery.Client
    project_id: str
    dataset: str

    def load_table(self, df, table_name):
        table_id = f"{self.project_id}.{self.dataset}.{table_name}"

        job_config = bigquery.LoadJobConfig(
            write_disposition="WRITE_TRUNCATE",
        )

        # Upload DataFrame to BigQuery
        job = self.client.load_table_from_dataframe(df, table_id, job_config=job_config)
        job.result()  # Wait for the job to complete

    def get_table(self, table_name):
        table_id = f"{self.project_id}.{self.dataset}.{table_name}"
        # Check if table was created or overwritten
        table = self.client.get_table(table_id)
        return table

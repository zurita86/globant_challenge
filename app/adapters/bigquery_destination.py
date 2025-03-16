from dataclasses import dataclass
from google.cloud import bigquery

from app.ports.db_destination import DestinationInterface


@dataclass
class BQDestination(DestinationInterface):
    client: bigquery.Client

    def load_table(self, df, table_id):
        # Upload DataFrame to BigQuery
        job = self.client.load_table_from_dataframe(df, table_id)
        job.result()  # Wait for the job to complete

    def get_table(self, table_id):
        # Check if table was created or overwritten
        table = self.client.get_table(table_id)
        return table

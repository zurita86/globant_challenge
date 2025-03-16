from dataclasses import dataclass
from fastapi import UploadFile, HTTPException
import pandas as pd
import json
import io

from app.ports.file_parser import FileParser


@dataclass
class ParseCSV(FileParser):
    file: UploadFile

    async def parse_as_df(self, headers=None):
        # Read the CSV file
        contents = await self.file.read()
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

        return df

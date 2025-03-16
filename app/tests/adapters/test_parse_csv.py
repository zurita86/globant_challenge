import pytest
import io
import json
from fastapi import UploadFile, HTTPException
from app.adapters.parse_csv import ParseCSV  # Adjust import based on your project structure


@pytest.mark.asyncio
async def test_parse_csv_with_headers():
    csv_content = "5,VP Marketing\n5,VP Marketing"
    file = UploadFile(filename="test.csv", file=io.BytesIO(csv_content.encode("utf-8")))
    headers = json.dumps(["id", "job"])

    parser = ParseCSV(file)
    df = await parser.parse_as_df(headers=headers)

    assert list(df.columns) == ["id", "job"]
    assert df.shape == (1, 2)  # Two data rows


@pytest.mark.asyncio
async def test_parse_csv_invalid_json_headers():
    csv_content = "5,VP Marketing\n5,VP Marketing"
    file = UploadFile(filename="test.csv", file=io.BytesIO(csv_content.encode("utf-8")))
    headers = "invalid-json"

    parser = ParseCSV(file)
    with pytest.raises(HTTPException) as excinfo:
        await parser.parse_as_df(headers=headers)

    assert excinfo.value.status_code == 400
    assert "Invalid headers format" in excinfo.value.detail


@pytest.mark.asyncio
async def test_parse_csv_mismatched_headers():
    csv_content = "5,VP Marketing\n5,VP Marketing"
    file = UploadFile(filename="test.csv", file=io.BytesIO(csv_content.encode("utf-8")))
    headers = json.dumps(["id"])

    parser = ParseCSV(file)
    with pytest.raises(HTTPException) as excinfo:
        await parser.parse_as_df(headers=headers)

    assert excinfo.value.status_code == 400
    assert "Number of headers (1) does not match number of columns in CSV (2)" in excinfo.value.detail


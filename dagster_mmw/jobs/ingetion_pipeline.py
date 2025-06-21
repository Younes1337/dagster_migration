import pandas as pd # type: ignore
from dagster import op, job # type: ignore

@op
def load_json_from_blob_op(context):
    context.log.info("Mock: Loading JSON files from Azure Blob Storage...")
    # Return dummy data
    return pd.DataFrame([{"id": 1, "value": "dummy"}])

@op
def ingest_to_snowflake_op(context, data: pd.DataFrame):
    context.log.info(f"Mock: Ingesting {len(data)} records into Snowflake...")
    # Return the same data (mocked)
    return data

@op
def trigger_dbt_blue_green_op(context, data: pd.DataFrame):
    context.log.info("Mock: Triggering DBT blue-green deployment...")
    # No real action, just log

@job
def nightly_ingest_job():
    data = load_json_from_blob_op()
    loaded = ingest_to_snowflake_op(data)
    trigger_dbt_blue_green_op(loaded)
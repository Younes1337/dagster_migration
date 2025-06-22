# fmt: off
from dagster import Definitions, load_assets_from_modules # type: ignore
from dagster_dbt import load_assets_from_dbt_project # type: ignore
import os

from .assets import test_asset
from .jobs import ingetion_pipeline

test_assets = load_assets_from_modules([test_asset])

dbt_assets = load_assets_from_dbt_project(
    project_dir=os.path.join(os.path.dirname(__file__), '..', 'transformations'),
    profiles_dir=os.path.join(os.path.dirname(__file__), '..', 'transformations'),
)

defs = Definitions(
    assets=[*test_assets, *dbt_assets],
    jobs=[ingetion_pipeline.nightly_ingest_job],
)
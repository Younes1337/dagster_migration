# fmt: off
from dagster import Definitions, load_assets_from_modules # type: ignore
from .assets import test_asset
from .jobs import ingetion_pipeline

test_assets = load_assets_from_modules([test_asset])

defs = Definitions(
    assets=[*test_assets],
    jobs=[ingetion_pipeline.nightly_ingest_job]
)
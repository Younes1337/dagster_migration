# fmt: off
from dagster import Definitions, load_assets_from_modules # type: ignore

from .assets import test_asset

test_assets = load_assets_from_modules([test_asset])

defs = Definitions(
    assets=[*test_assets]
)

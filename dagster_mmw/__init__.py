# fmt: off
from dagster import Definitions, load_assets_from_modules, AssetExecutionContext # type: ignore
from .assets import test_asset
from .jobs import ingetion_pipeline
from pathlib import Path
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets


# Points to the dbt project path
dbt_project_directory = Path(__file__).parent.parent / "transformations"
dbt_project = DbtProject(project_dir=dbt_project_directory)

# References the dbt project object
dbt_resource = DbtCliResource(project_dir=dbt_project)

# Compiles the dbt project & allow Dagster to build an asset graph
dbt_project.prepare_if_dev()


# Yields Dagster events streamed from the dbt CLI
@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build", "--target", "prod"], context=context).stream()

test_assets = load_assets_from_modules([test_asset])

defs = Definitions(
    assets=[dbt_models],
    jobs=[ingetion_pipeline.demo_blue_green_pipeline],
    resources={"dbt": dbt_resource}
)
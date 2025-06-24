import pandas as pd  # type: ignore
import random
from datetime import datetime, timedelta
from dagster import op, job # type: ignore
from dagster_dbt import DbtCliResource # type: ignore

@op
def load_dynamic_orders_data(context):
    customers = ["Acme", "Beta", "Gamma", "Delta", "Epsilon", "Zeta", "Eta", "Theta", "Iota", "Kappa"]
    base_date = datetime.now().date()
    data = []
    for i in range(1, 11):
        order = {
            "order_id": i,
            "customer": random.choice(customers),
            "amount": random.randint(80, 350),
            "order_date": (base_date - timedelta(days=random.randint(0, 5))).isoformat(),
            "processed": random.choice([True, False])
        }
        data.append(order)
    df = pd.DataFrame(data)
    context.log.info(f"Generated {len(df)} dynamic orders.")
    context.log.info(f"Sample: {df.head(3).to_dict(orient='records')}")
    return df

@op
def process_and_ingest(context, data: pd.DataFrame):
    context.log.info("Processing and ingesting data (dummy)...")
    data['processed'] = True
    context.log.info(f"Processed data sample: {data.head(3).to_dict(orient='records')}")
    return data


@op(required_resource_keys={"dbt"})
def blue_green_deploy(context, data):
    # Step 1: Build in green
    context.log.info("Building dbt models in green (staging) schema...")
    build_result = context.resources.dbt.cli(["build", "--target", "prod"], context=context)
    for event in build_result.stream():
        context.log.info(event)
    # Step 2: Test in green
    context.log.info("Testing dbt models in green (staging) schema...")
    test_result = context.resources.dbt.cli(["test", "--target", "prod"], context=context)
    for event in test_result.stream():
        context.log.info(event)
    # Step 3: Swap schemas (you need a macro or SQL for this)
    context.log.info("Swapping green schema to become production (blue)...")
    # Example: context.resources.dbt.cli(["run-operation", "swap_schemas"], context=context)
    # Step 4: Cleanup old green
    context.log.info("Cleaning up old green schema...")
    # Example: context.resources.dbt.cli(["run-operation", "drop_old_green"], context=context)
    context.log.info("Blue-green deployment complete.")
    return "success"


@job
def demo_blue_green_pipeline():
    data = load_dynamic_orders_data()
    processed = process_and_ingest(data)
    blue_green_deploy(processed)
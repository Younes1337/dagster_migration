from dagster import asset # type: ignore

@asset 
def test_asset():
    return "Hello, Dagster!"
    
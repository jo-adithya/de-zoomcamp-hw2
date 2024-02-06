import pandas as pd

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data: pd.DataFrame, *args, **kwargs):
    data = data[data["passenger_count"] > 0]
    data = data[data["trip_distance"] > 0]
    data["lpep_pickup_datetime"] = pd.to_datetime(data["lpep_pickup_datetime"])
    data["lpep_pickup_date"] = data["lpep_pickup_datetime"].dt.date
    data.columns = (
        data.columns.str.replace(" ", "_")
        .str.replace("(?<=[a-z])(?=[A-Z])", "_", regex=True)
        .str.lower()
    )

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
    assert "vendor_id" in output.columns, "vendor_id is not in output data"
    assert (
        output["passenger_count"].eq(0).sum() == 0
    ), "There are rows with zero passengers in the output data."
    assert (
        output["trip_distance"].eq(0).sum() == 0
    ), "There are rows with zero trip distance in the output data."
    print(output["vendor_id"].unique())

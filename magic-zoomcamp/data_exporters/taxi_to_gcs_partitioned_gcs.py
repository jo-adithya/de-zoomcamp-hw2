import pyarrow as pa
import pyarrow.parquet as pq
from pandas import DataFrame
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/src/mage-zoomcamp-413305-390d6ba4a1fe.json"

bucket_name = 'mage-zoomcamp-413305'
project_id = 'mage-zoomcamp-413305'

table_name = "nyc_taxi_data"

root_path = f"{bucket_name}/{table_name}"

@data_exporter
def export_data_to_google_cloud_storage(df: DataFrame, **kwargs) -> None:
    df["tpep_pickup_date"] = df["tpep_pickup_datetime"].dt.date

    table = pa.Table.from_pandas(df)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path=root_path,
        partition_cols=["tpep_pickup_date"],
        filesystem=gcs
    )

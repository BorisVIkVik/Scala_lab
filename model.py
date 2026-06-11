# from pyspark.sql import SparkSession
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
# from pyspark.pandas import read_parquet
from delta import configure_spark_with_delta_pip
# import requests

# resp = requests.post("http://scala-server:8080/run-job", json={
#     "dataset": "features_v1"
# })

# print(resp.text)
os.environ["PYARROW_IGNORE_TIMEZONE"] = "1" 
spark = configure_spark_with_delta_pip(SparkSession.builder.appName("MyApp").master("local[*]") \
     .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.maxResultSize", "2g") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "8") \
    .config("spark.default.parallelism", "8") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.sql.files.maxPartitionBytes", "64m") \
    .config("spark.sql.files.openCostInBytes", "4194304") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")).getOrCreate()
# spark = configure_spark_with_delta_pip(builder)
df = spark.read.format('delta').load('./resources/output_data')
df.show(truncate=False)
from delta.tables import DeltaTable

path = "./resources/output_data"

dt = DeltaTable.forPath(spark, path)

history = dt.history(1)
history.show(truncate=False)
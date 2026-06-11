# from pyspark.sql import SparkSession
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
# from pyspark.pandas import read_parquet
from delta import configure_spark_with_delta_pip

from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/api/endpoint', methods=['POST'])
def handle_post():
    data = request.json
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
    df = spark.read.format('delta').load('./resources/output_data')
    from delta.tables import DeltaTable

    path = "./resources/output_data"

    dt = DeltaTable.forPath(spark, path).toDF()
    dt.show(truncate=False)
    # history = dt.history(1)
    # history.show(truncate=False)

    # df2 = assembler.transform(df.fillna(0, subset=["with_sweeteners"]))
    # del df
    assembler = VectorAssembler(
    inputCols=["known_ingredients_n"],
    outputCol="features"
)

    df2 = assembler.transform(df)
    kmeans = KMeans(featuresCol='features',k=2)
    model = kmeans.fit(df2)
    predictions = model.transform(df2)

    centers = model.clusterCenters()
    print("Cluster Centers: ")
    for center in centers:
        print(center)
    # df = spark.createDataFrame(centers, IntegerType())
    # df.write.mode("overwrite").csv("hdfs://namenode:8020/test/output.csv")
    # print(spark)
    spark.stop()
    return {'status': 'ok'}


if __name__ == '__main__':
    app.run(port=5000)

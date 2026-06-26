import os
import yaml
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
from delta import configure_spark_with_delta_pip
from delta.tables import DeltaTable

def clasterisation():
    with open('config/app_spark_config.yaml') as f:
        cfg = yaml.safe_load(f)

    os.environ["PYARROW_IGNORE_TIMEZONE"] = "1" 
    builder = SparkSession.builder.appName(cfg['spark']['app_name']).master(cfg['spark']['master'])
        

    for key, value in cfg['spark']['configs'].items():
        builder = builder.config(key, value)


    spark = configure_spark_with_delta_pip(builder).getOrCreate()

    df = spark.read.format('delta').load('resources/output_data')
    

    path = "resources/output_data"

    dt = DeltaTable.forPath(spark, path).toDF()
    dt.show(truncate=False)

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

    print(df.count())

    spark.stop()
    return centers
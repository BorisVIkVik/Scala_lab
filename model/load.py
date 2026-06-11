# from pyspark.sql import SparkSession
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import IntegerType
from pyspark.ml.clustering import KMeans
from pyspark.ml.feature import VectorAssembler
# from pyspark.pandas import read_parquet
os.environ["PYARROW_IGNORE_TIMEZONE"] = "1" 
spark = SparkSession.builder.appName("MyApp").master("local[*]") \
     .config("spark.driver.memory", "8g") \
    .config("spark.executor.memory", "2g") \
    .config("spark.driver.maxResultSize", "2g") \
    .config("spark.sql.adaptive.enabled", "true") \
    .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
    .config("spark.sql.shuffle.partitions", "16") \
    .config("spark.default.parallelism", "16") \
    .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer") \
    .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
    .config("spark.sql.files.maxPartitionBytes", "256m") \
    .config("spark.sql.files.openCostInBytes", "4194304") \
    .config("spark.hadoop.dfs.client.use.datanode.hostname", "true") \
    .config("spark.hadoop.dfs.datanode.use.datanode.hostname", "true") \
    .getOrCreate()
df = spark.read.parquet('/Users/bw/GITS/ITMO/Scala_Lab/data/food.parquet').limit(1000)

# df1 = spark.createDataFrame(df)
# df = df
# df_single = df.select("with_sweeteners").dropna()
# # del df
# print()
# df.show()
# print(f'Hello count: {df_single.count()}')
# # del df_single

# assembler = VectorAssembler(
#     inputCols=["with_sweeteners"],
#     outputCol="features"
# )

# df2 = assembler.transform(df.fillna(0, subset=["with_sweeteners"]))
# # del df
# kmeans = KMeans(featuresCol='features',k=2)
# model = kmeans.fit(df2)
# predictions = model.transform(df2)

# centers = model.clusterCenters()
# print("Cluster Centers: ")
# for center in centers:
#     print(center)
# df = spark.createDataFrame(centers, IntegerType())
df.write.mode("overwrite").parquet("hdfs://localhost:8020/test/output.parquet")
print(spark)
spark.stop()
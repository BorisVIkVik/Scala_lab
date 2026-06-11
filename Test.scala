import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SparkSession 
object FileDemo {
  def main(args: Array[String]): Unit = {
    val conf = new SparkConf()
      .setAppName("FileReaderDemo")
      .setMaster("local[2]") 
      .set("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
      .set("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
      .set("spark.jars.packages", "io.delta:delta-core_2.12:2.2.0") 
      .set("spark.hadoop.dfs.client.use.datanode.hostname", "true") 
      .set("spark.hadoop.dfs.datanode.use.datanode.hostname", "true") 
    
    val sc = new SparkContext(conf)
    sc.setLogLevel("WARN")
    // val df = sc.textFile("/Users/bw/GITS/ITMO/Scala_Lab/data/food.parquet")
    
  


     val spark = SparkSession.builder().config(conf).getOrCreate()
  
    import spark.implicits._
    println("Начинаю загрузку!")
    val df = spark.read.parquet("hdfs://localhost:8020/test/output.parquet")
    println("Данные успешно загружены!")
    val tmp = df.select("known_ingredients_n")
    

    val df_col = tmp.na.drop()
    // val df = lines.toDF("line_text")
    println("Колонка извлечена")

    df_col.write
      
      .format("delta")
      .save("")
    val query = df_col.writeStream
    .mode("overwrite")
    .format("delta")                         // Target storage format
    .outputMode("append")                      // Business logic for updates
    .option("checkpointLocation", "path/chk/") // Crucial for fault tolerance
    .option("path", "./resources/output_data")            // Destination path
    .start()   
    println("Данные успешно записаны в формат Delta!")

    // val df_test = spark.read.format("delta").load("./resources/output_data")
    // val df_kek = df_test.toDF()

    // df_kek.printSchema()

    // tmp.show(truncate = false)

    // df_kek.show(truncate = false)
    

    println(tmp.count())
    println(df_kek.count())

    sc.stop()
  }
}
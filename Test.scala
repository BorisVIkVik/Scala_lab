
import akka.actor.ActorSystem
import akka.http.scaladsl.client.RequestBuilding.Post
import akka.http.scaladsl.model.{ContentTypes, HttpEntity}
import scala.concurrent.ExecutionContext
import scala.concurrent.ExecutionContext.Implicits.global
import akka.http.scaladsl.Http
import scala.concurrent.Await
import scala.concurrent.duration._



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
      .mode("overwrite")
      .format("delta")                           
      .save("./resources/output_data")
    // val query = df_col.writeStream
    implicit val system = ActorSystem("client")
    val myBool = true

    val request = Post("http://127.0.0.1:5000/api/endpoint", s"""{"bool":$myBool}""")
      .withEntity(HttpEntity(ContentTypes.`application/json`, s"""{"bool":$myBool}"""))
    println("Отправляю python!")
    // .outputMode("append")                      // Business logic for updates
    // .option("checkpointLocation", "path/chk/") // Crucial for fault tolerance
    // .option("path", "")            // Destination path
    // .start()   
    // query.awaitTermination()  
    val response = Await.result(Http().singleRequest(request), 180.seconds)
    println(s"Ответ сервера: ${response.status}")
    
    
    tmp.show(truncate = false)

    df_col.show(truncate = false)
    

    println(tmp.count())
    println(df_col.count())
    sc.stop()
    spark.stop()
    Http().shutdownAllConnectionPools()
    system.terminate()
    Await.result(system.whenTerminated, 10.seconds)
    // val df_test = spark.read.format("delta").load("./resources/output_data")
    // val df_kek = df_test.toDF()

    // df_kek.printSchema()


  }
}
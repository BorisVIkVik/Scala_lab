// FileDemo.scala - полное Spark-приложение на Scala
import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.SparkSession 
object FileDemo {
  def main(args: Array[String]): Unit = {
    // 1. Создаем Spark конфигурацию
    val conf = new SparkConf()
      .setAppName("FileReaderDemo")
      .setMaster("local[2]") // локальный режим с 2 потоками
    
    // 2. Создаем SparkContext
    val sc = new SparkContext(conf)
    
    // 3. Чтение текстового файла
    val lines = sc.textFile("/Users/bw/GITS/ITMO/Scala_Lab/kek.txt")
    
    // 4. Подсчет строк
    val lineCount = lines.count()
    println(s"Количество строк в файле: $lineCount")
    
    // 5. Вывод всех строк
    println("Содержимое файла:")
    lines.foreach(println)


     val spark = SparkSession.builder().config(conf).getOrCreate()
    
    // Импортируем магия .toDF() для преобразования RDD в DataFrame
    import spark.implicits._
    // val df = lines.toDF()
    // df.write
    //   .mode("overwrite")
    //   .parquet("./resources/output_data")

    val df = lines.toDF("line_text")
    
    // Записываем DataFrame в формате Parquet
    df.write
      .mode("overwrite")
      .parquet("./resources/output_data")

    println("Данные успешно записаны в формат Parquet!")

    val df_kek = spark.read.parquet("./resources/output_data")

    // 3. Выводим схему (структуру колонок), чтобы убедиться в корректности
    df_kek.printSchema()

    // 4. Показываем первые 20 строк из всех партиций
    df_kek.show(truncate = false)
    
    // 6. Завершение SparkContext
    sc.stop()
  }
}
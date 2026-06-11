name := "TestSpark"
version := "1.0"
libraryDependencies += "org.apache.spark" %% "spark-core" % "3.4.0"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.4.0"
libraryDependencies += "io.delta" %% "delta-core" % "2.4.0"

// Разрешаем запуск в отдельном процессе (Fork)
fork := true

// Передаем флаги компилятора и JVM для открытия доступа к внутренним пакетам Java
javaOptions ++= Seq(
  "--add-exports=java.base/sun.nio.ch=ALL-UNNAMED",
  "--add-opens=java.base/sun.nio.ch=ALL-UNNAMED",
  "--add-opens=java.base/java.nio=ALL-UNNAMED"
)

// Направляет лог-потоки напрямую в консоль без префиксов sbt
outputStrategy := Some(StdoutOutput)

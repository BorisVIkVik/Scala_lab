# Викторов Борис Лабораторная 5.

Работа посвящена pyspark и Scala витрине.

## Данные: OpenFoodFacts
https://huggingface.co/datasets/openfoodfacts/product-database

## Модель: KMeans

## Database/FileSystem: HDFS

## Структура
```
.
├── config
├── data
├── hadoop
│   └── test.sh
└── src

```
Папки:

    config: Хранится yaml файл с конфигурацией pyspark.
    data: Хранится parquet с данными.
    src: Папка для кода модели.
    hadoop: Папка для кода hdfs с docker.
## Запуск
HDFS:
    docker compose -f ./hadoop/docker-compose.yaml --project-directory ./hadoop up -d
Когда HDFS загружен запускаем код для загрузки данных:
    python src/load.py
После запускаем Flask сервер:
    python main.py
Дальше запускаем Scala витрину:
    sbt run
    


# Databricks notebook source
from pyspark.sql import functions as f

# COMMAND ----------

aws_bucket_name = "dataeng-landing-zone-957"

df = spark.read.format("csv").option("header", True).option("inferSchema", True).option("sep", ';').load(f"s3://{aws_bucket_name}/big_data_ada/temas_ambientais.csv")
display(df)


# COMMAND ----------

spark.sql("create database if not exists bronze;")

# COMMAND ----------

(
    df
    .withColumn("ano_inscricao", f.year("data_inscricao"))
    .write
    .format("delta")
    .mode("overwrite")
    .option("maxRecordsPerFile", 1_000_000)
    .option("compression", 'snappy')
    .partitionBy("uf", "ano_inscricao")
    .option("path", f"s3://{aws_bucket_name}/big_data_ada/bronze/temas_ambientais")
    .saveAsTable("bronze.temas_ambientais")
)


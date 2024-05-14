# Databricks notebook source
aws_bucket_name = 'dataeng-landing-zone-957'

# COMMAND ----------

temas_ambientais = spark.read.table("bronze.temas_ambientais")

# COMMAND ----------

temas_ambientais.count()

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create database if not exists silver;

# COMMAND ----------

(
    temas_ambientais
    .write
    .format("delta")
    .mode("overwrite")
    .option("maxRecordsPerFile", 1_000_000)
    .option("compression", 'snappy')
    .partitionBy("uf", "ano_inscricao")
    .option("path", f"s3://{aws_bucket_name}/big_data_ada/silver/temas_ambientais")
    .saveAsTable("silver.temas_ambientais")
)


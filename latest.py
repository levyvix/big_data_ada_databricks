# Databricks notebook source
dbutils.fs.mount()

# COMMAND ----------

url = "https://dados.agricultura.gov.br/dataset/58bdc09c-9778-42b9-8fce-7d5c2c4fa211/resource/daf8053b-5446-4cd4-986a-f141b4a434ec/download/temas_ambientais.csv"
query_parameters = {"downloadformat": "csv"}

# COMMAND ----------

import requests

# COMMAND ----------

response = requests.get(url, params=query_parameters)

# COMMAND ----------

response.status_code

# COMMAND ----------

with open("/tmp/temas_ambientais.csv", mode="wb") as file:
    file.write(response.content)

# COMMAND ----------

import pyspark.pandas as ps

# COMMAND ----------

temas = ps.read_csv("file:/tmp/temas_ambientais.csv", sep=';')

# COMMAND ----------

temas_spark = temas.to_spark()

# COMMAND ----------

temas_spark.display()

# COMMAND ----------

from pyspark.sql import functions as f

# COMMAND ----------

# %sql 

# create database bronze;

# COMMAND ----------

(temas_spark
    .withColumn("ano_inscricao", f.year("data_inscricao"))
    .write
    .format("delta")
    .mode("overwrite")
    .option("maxRecordsPerFile", 1_000_000)
    .option("compression", 'snappy')
    .partitionBy("uf", "ano_inscricao")
    .option("path", "/FileStore/tables/big_data_ada/bronze/temas_municipios")
    .saveAsTable("bronze.temas_municipios"))


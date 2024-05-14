# Databricks notebook source
from pyspark.sql import functions as f
from pyspark.sql.functions import isnan, when, count, col

# COMMAND ----------

aws_bucket_name = 'dataeng-landing-zone-957'

# COMMAND ----------

temas_ambientais = spark.read.table("silver.temas_ambientais")

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC create database  if not exists gold;

# COMMAND ----------

# MAGIC %md
# MAGIC # Consulta 1

# COMMAND ----------

consulta_1 = temas_ambientais.where("uf in ('MT', 'MS')").groupBy("uf").agg(
    f.sum("area_do_imovel").alias("soma_hectares")
).orderBy("soma_hectares", ascending=False)

consulta_1.display()

consulta_1.write.format("delta").mode("overwrite").option("path", f"s3://{aws_bucket_name}/big_data_ada/gold/soma_area_imovel_MT_MS").saveAsTable("gold.soma_area_imovel_MT_MS")

# COMMAND ----------

# MAGIC %md
# MAGIC # Consulta 2

# COMMAND ----------

consulta_2 = temas_ambientais.where("uf in ('ES', 'SP', 'RJ', 'MG')")

consulta_2.display()

consulta_2.write.format("delta").mode("overwrite").option("path", f"s3://{aws_bucket_name}/big_data_ada/gold/sudeste").saveAsTable("gold.sudeste")

# COMMAND ----------

# MAGIC %md
# MAGIC # Consulta 3

# COMMAND ----------

consulta_3 = temas_ambientais.groupBy("ano_inscricao").count().orderBy("ano_inscricao")
consulta_3.display()
consulta_3.write.format("delta").mode("overwrite").option("path", f"s3://{aws_bucket_name}/big_data_ada/gold/contagem_ano_inscricao").saveAsTable("gold.contagem_ano_inscricao")

# COMMAND ----------

# MAGIC %md
# MAGIC # Consulta 4

# COMMAND ----------

consulta_4 =( 
             temas_ambientais
             .withColumn("proporcao_vegetacao_remanescente", col("area_remanescente_vegetacao_nativa") / col("area_do_imovel"))
             .select(f.avg("proporcao_vegetacao_remanescente").alias("proporcao_vegetacao_remanescente"))
)
consulta_4.display()



consulta_4.write.format("delta").mode("overwrite").option("path", f"s3://{aws_bucket_name}/big_data_ada/gold/proporcao_vegetacao_remanescente").saveAsTable("gold.proporcao_vegetacao_remanescente")


# COMMAND ----------

# MAGIC %md
# MAGIC # Consulta 5

# COMMAND ----------

consulta_5 = temas_ambientais.groupBy("uf").count().orderBy("uf")
consulta_5.display()
consulta_5.write.format("delta").mode("overwrite").option("path", f"s3://{aws_bucket_name}/big_data_ada/gold/contagem_imoveis_uf").saveAsTable("gold.contagem_imoveis_uf")

# COMMAND ----------

# MAGIC %md
# MAGIC # Consulta 6

# COMMAND ----------

media_area_total = temas_ambientais.select(f.avg("area_do_imovel")).first()[0]

consulta_6 = propriedades_acima_da_media = temas_ambientais.filter("area_do_imovel > {}".format(media_area_total)) \
    .groupBy("uf") \
    .agg(f.count("municipio").alias("propriedades_acima_da_media")) \
    .orderBy("uf")
consulta_6.display()
consulta_6.write.format("delta").mode("overwrite").option("path", f"s3://{aws_bucket_name}/big_data_ada/gold/imoveis_acima_media").saveAsTable("gold.imoveis_acima_media")

# COMMAND ----------



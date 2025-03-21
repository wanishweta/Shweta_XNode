from pyspark.sql import SparkSession
import pyspark

from pyspark.sql.types import *
from pyspark.sql.functions import *

spark = (
    SparkSession
    .builder
    .appName("DeltaLakeApp")

    .master("local[4]")


    .getOrCreate()
)

print(pyspark.__version__)
print(spark.version)

df = spark.sql("""

CREATE DATABASE IF NOT EXISTS TaxisDB

""")

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Tables with important attributes
# ozone = glueContext.create_dynamic_frame.from_catalog(database = "1strategy-insights-dm", table_name = "insights_dm_stage_cached_applications", transformation_ctx = "applications")
ozone = glueContext.create_dynamic_frame_from_options("mysql", connection_options = {"url": "jdbc:mysql://air-quality.crwizazpv2rg.us-west-2.rds.amazonaws.com:3306/airquality", "user": "etl", "password": "thisismysupersecretpassword", "dbtable": "ozone"}, format=None)

# Create Data Frames and Views to query
ozone_df = ozone.toDF()
ozone_df.createOrReplaceTempView("ozone_view")

utah_subset_query = """
select * from ozone where state = 'utah';
"""

utah_ozone = spark.sql(utah_subset_query)

# JOIN Data here


# Recreate Dynamic Frame to write to S3
utah_ozone_dynamic = DynamicFrame.fromDF(utah_ozone, glueContext, "utah_ozone_dynamic")

datasink2 = glueContext.write_dynamic_frame.from_options(frame = utah_ozone_dynamic, connection_type = "s3", connection_options = {"path": "s3://1s-sagemaker-demos/airquality/utah/", "compression": "gzip"}, format = "csv", transformation_ctx = "utah_ozone_dynamic")

job.commit()
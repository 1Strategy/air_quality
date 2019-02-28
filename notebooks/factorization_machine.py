#%%
import sagemaker
import os
import boto3
import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


if sys.version_info[0] < 3: 
    from StringIO import StringIO # Python 2.x
else:
    from io import StringIO # Python 3.x

# get your credentials from environment variables
aws_id = os.environ['AWS_ID']
aws_secret = os.environ['AWS_SECRET']

client = boto3.client('s3', aws_access_key_id=aws_id,
        aws_secret_access_key=aws_secret)

bucket_name = 'my_bucket'

object_key = 'my_file.csv'
csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
body = csv_obj['Body']
csv_string = body.read().decode('utf-8')

df = pd.read_csv(StringIO(csv_string))



#%%

ozone = pd.read_csv(
    "/Users/alexgraves/Desktop/airquality/ozone_per_day.csv"
)
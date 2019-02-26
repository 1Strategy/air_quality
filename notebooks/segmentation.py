#%%
import sagemaker
import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#%%

ozone = pd.read_csv(
    "/Users/alexgraves/Desktop/airquality/ozone_per_day.csv"
)
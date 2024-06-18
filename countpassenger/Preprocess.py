import pandas as pd
import numpy as np
import os
from countpassenger.Config import conf

drop_label_vehicle = ['car_brand_model',
              'vehicle_type_model',
              'plate_number_definition',
              'plate_representative_vehicle_image_name',
              'parent_image_name',
              'full_image_names',
              'timestamp',
              ]

important_label_vehicle = [
    'timestamp_precise', 
]

def df_clean_vehicle(df_vehicle: pd.DataFrame, drop_na:list = ['plate_number'] ,drop_label: list = None):
    filtered_vehicle = None
    filtered_vehicle = df_vehicle.dropna(subset=drop_na)
    #clean up camera_name to camera_clean
    #drop N/A plate number
    #filter to only van and bus
    return filtered_vehicle

# def df_clean_cross(df_customer: pd.DataFrame):
#     return filtered_customer


print(conf.BASE_DIR)
import pandas as pd
import numpy as np
import os
from countpassenger.Config import conf

drop_label_vehicle = [
    "car_brand_model",
    "vehicle_type_model",
    "plate_number_definition",
    "plate_representative_vehicle_image_name",
    "parent_image_name",
    "full_image_names",
    "timestamp",
]

IMPORTANT_LABEL_VEHICLE = [
    "timestamp_precise",
    "camera-cleaned",
    "plate_number",
    "lifetime",
    "vehicle_type",
    "xmin",
    "xmax",
    "ymin",
    "ymax",
]


def df_clean_vehicle(
    df_vehicle: pd.DataFrame,
    drop_na: list = ["plate_number"],
    drop_label: list = None,
    included_vehicle_type: list = ["van", "bus"],
):
    filtered_vehicle = None
    # drop N/A plate number
    # filter to only van and bus
    # clean up camera_name to camera_clean
    filtered_vehicle = df_vehicle.dropna(subset=drop_na)
    filtered_vehicle = filtered_vehicle[
        filtered_vehicle["vehicle_type"].isin(included_vehicle_type)
    ]
    filtered_vehicle["camera_cleaned"] = filtered_vehicle["camera"].str.extract(
        r"^(mbk-\d{2}-\d{2})"
    )

    filtered_vehicle = convert_series_to_datetime(filtered_vehicle)

    return filtered_vehicle


def create_unix_column(df: pd.DataFrame):
    # Convert to datetime
    df["timestamp_unix"] = pd.to_datetime(df["timestamp_precise"], format="ISO8601")

    df["lifetime_unix"] = pd.to_datetime()

    return df


# def convert_lifetime_to_datetime


print(conf.BASE_DIR)

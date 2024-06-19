import pandas as pd
import numpy as np
import os
from countpassenger.Config import conf

DROP_LABEL_VEHICLE = [
    "car_brand_model",
    "vehicle_type_model",
    "plate_number_definition",
    "plate_representative_vehicle_image_name",
    "parent_image_name",
    "full_image_names",
    "_id",
    "id",
    "tracking_id",
    "count_id",
]

DROP_LABEL_CUSTOMER = [
    "_id",
    "id",
    "tracking_id",
    "count_id",
    "full_image_names",
    "parent_image_name",
    "image_name",
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
    drop_na: list = [],
    drop_label: list = DROP_LABEL_VEHICLE,
    included_vehicle_type: list = ["van", "bus", "truck"],
):
    # drop N/A plate number
    # filter to only van and bus
    # clean up camera_name to camera_clean
    filtered_vehicle = df_vehicle.dropna(subset=drop_na)
    filtered_vehicle = filtered_vehicle.drop(labels=drop_label, axis=1)
    filtered_vehicle = filtered_vehicle[
        filtered_vehicle["vehicle_type"].isin(included_vehicle_type)
    ]
    filtered_vehicle["camera_cleaned"] = filtered_vehicle["camera"].str.extract(
        r"^(mbk-\d{2}-\d{2})"
    )

    filtered_vehicle = format_datetime_column(filtered_vehicle)

    return filtered_vehicle


def df_clean_customer(
    df_customer: pd.DataFrame,
    drop_na: list = [],
    drop_label: list = DROP_LABEL_CUSTOMER,
):
    # filter drop_labels
    # clean up camera_name to camera_clean
    filtered_customer = df_customer.dropna(subset=drop_na)
    filtered_customer = filtered_customer.drop(labels=drop_label, axis=1)
    filtered_customer["camera_cleaned"] = filtered_customer["camera"].str.extract(
        r"^(mbk-\d{2}-\d{2})"
    )

    filtered_customer = format_datetime_column(filtered_customer)

    return filtered_customer


def format_datetime_column(df: pd.DataFrame):
    # Convert to datetime
    df["timestamp_precise"] = pd.to_datetime(df["timestamp_precise"], format="ISO8601")
    df["timestamp_unix"] = (df["timestamp_precise"] - pd.Timestamp("1970-01-01")) // pd.Timedelta(
        "1s"
    )

    return df


# def convert_lifetime_to_datetime


print(conf.BASE_DIR)

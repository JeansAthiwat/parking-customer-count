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
    convert_truck: bool = True,
):
    # drop N/A plate number
    # filter to only van and bus
    # clean up camera_name to camera_clean
    filtered_vehicle = df_vehicle.dropna(subset=drop_na)
    filtered_vehicle = filtered_vehicle.drop(labels=drop_label, axis=1)
    # filtered_vehicle = filtered_vehicle[
    #     filtered_vehicle["vehicle_type"].isin(included_vehicle_type)
    # ]
    if convert_truck:
        filtered_vehicle = truck_to_bus(filtered_vehicle, threshold=0.8)

    filtered_vehicle["camera_cleaned"] = filtered_vehicle["camera"].str.extract(
        r"^(mbk-\d{2}-\d{2})"
    )

    filtered_vehicle = format_datetime_column(filtered_vehicle)

    # add end time stamp
    filtered_vehicle["timestamp_unix_end"] = (
        filtered_vehicle["timestamp_unix"] + (filtered_vehicle["lifetime"].astype(np.int64))
    ).astype(np.int64)

    return filtered_vehicle


def truck_to_bus(df_vehicle: pd.DataFrame, threshold: float = 0.8):
    """if predict type as truck it might actually be a bus u know"""
    df_vehicle.loc[
        (df_vehicle["vehicle_type"] == "truck") & (df_vehicle["vehicle_type_confidence"] < 0.6),
        "vehicle_type",
    ] = "bus"
    return df_vehicle


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
    df["timestamp_unix"] = (
        (df["timestamp_precise"] - pd.Timestamp("1970-01-01")) // pd.Timedelta("1s")
    ).astype(np.int64)

    return df


def filter_camera(df: pd.DataFrame, camera_name: str):
    df = df[df["camera"] == camera_name]
    return df


def sort_df(df: pd.DataFrame, sort_conditions: list):
    return df.sort_values(by=sort_conditions)


# print(conf.BASE_DIR)

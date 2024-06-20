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
    filter_vehicle=False,
    included_vehicle_type: list = ["van", "bus", "truck"],
    convert_truck: bool = True,
):

    filtered_vehicle = df_vehicle.dropna(subset=drop_na)  # drop N/A plate number
    filtered_vehicle = filtered_vehicle.drop(labels=drop_label, axis=1)

    if filter_vehicle:  # filter to only van and bus
        filtered_vehicle = filtered_vehicle[
            filtered_vehicle["vehicle_type"].isin(included_vehicle_type)
        ]

    if convert_truck:  # Convert unconfident type as desired
        filtered_vehicle = truck_to_bus(filtered_vehicle, threshold=0.8)

    filtered_vehicle["camera_cleaned"] = filtered_vehicle["camera"].str.extract(
        r"^(mbk-\d{2}-\d{2})"
    )  # clean up camera_name to camera_clean

    filtered_vehicle = calculate_bbox_midpoint(filtered_vehicle)
    filtered_vehicle = format_datetime_column(filtered_vehicle)  # format to datetime obj
    filtered_vehicle = calculate_timestamp_unix_end(filtered_vehicle)

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
    filtered_customer = df_customer.dropna(subset=drop_na)  # drop N/A frame
    filtered_customer = filtered_customer.drop(labels=drop_label, axis=1)  # filter drop_labels
    filtered_customer["camera_cleaned"] = filtered_customer["camera"].str.extract(
        r"^(mbk-\d{2}-\d{2})"
    )  # clean up camera_name to camera_clean

    filtered_customer = format_datetime_column(filtered_customer)
    filtered_customer = calculate_bbox_midpoint(filtered_customer)

    return filtered_customer


def calculate_bbox_midpoint(df: pd.DataFrame):
    # Calculate the midpoints
    df["xmid"] = (df["xmin"] + df["xmax"]) / 2
    df["ymid"] = (df["ymin"] + df["ymax"]) / 2

    # Append the new columns to the DataFrame
    df = df[["xmin", "xmax", "ymin", "ymax", "xmid", "ymid"]]
    return df


def calculate_timestamp_unix_end(df: pd.DataFrame):
    df["timestamp_unix_end"] = (df["timestamp_unix"] + (df["lifetime"].astype(np.int64))).astype(
        np.int64
    )
    return df


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

import pandas as pd
import numpy as np
import os
from countpassenger.Config import conf
from datetime import timedelta


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
    df_vehicle_raw: pd.DataFrame,
    drop_na: list = [],
    drop_label: list = DROP_LABEL_VEHICLE,
    current_camera: str = None,
    filter_vehicle=False,
    included_vehicle_type: list = ["van", "bus", "truck"],
    convert_truck: bool = True,
):

    assert current_camera, "the current camera name is wrong"
    camera_name = current_camera + "-vehicle"

    filtered_vehicle = df_vehicle_raw.dropna(subset=drop_na)  # drop N/A plate number
    filtered_vehicle = filtered_vehicle.drop(labels=drop_label, axis=1)

    if filter_vehicle:  # filter to only van and bus
        filtered_vehicle = filtered_vehicle[filtered_vehicle["vehicle_type"].isin(included_vehicle_type)]

    if convert_truck:  # Convert unconfident type as desired
        filtered_vehicle = truck_to_bus(filtered_vehicle, threshold=0.8)

    filtered_vehicle = calculate_bbox_midpoint(filtered_vehicle)
    filtered_vehicle = format_datetime_column(filtered_vehicle)  # format to datetime obj
    filtered_vehicle = calculate_timestamp_end(filtered_vehicle)

    filtered_vehicle = filter_camera(filtered_vehicle, camera_name)
    filtered_vehicle = sort_df(filtered_vehicle, conf.VEHICLE_INTEREST_NON_SNAPSHOT)

    return filtered_vehicle


def calculate_timestamp_end(df: pd.DataFrame):
    df["timestamp_unix_end"] = (df["timestamp_unix"] + (df["lifetime"].astype(np.int64))).astype(
        np.int64
    )  # add end time stamp
    return df


def truck_to_bus(df_vehicle: pd.DataFrame, threshold: float = 0.8):
    """if predict type as truck it might actually be a bus u know"""
    df_vehicle.loc[
        (df_vehicle["vehicle_type"] == "truck") & (df_vehicle["vehicle_type_confidence"] < 0.6),
        "vehicle_type",
    ] = "bus"
    return df_vehicle


def df_clean_customer(
    df_customer: pd.DataFrame,
    current_cam: str = None,
    drop_na: list = [],
    drop_label: list = DROP_LABEL_CUSTOMER,
):

    filtered_customer = df_customer.dropna(subset=drop_na)  # drop N/A frame
    filtered_customer = filtered_customer.drop(labels=drop_label, axis=1)  # filter drop_labels

    filtered_customer = calculate_bbox_midpoint(filtered_customer)
    filtered_customer = format_datetime_column(filtered_customer)

    assert current_cam, "current cam is not defined"

    filtered_customer = filter_camera(filtered_customer, camera_name=current_cam)
    filtered_customer = sort_df(filtered_customer, conf.CUSTOMER_INTEREST_SNAPSHOT)

    return filtered_customer


def calculate_bbox_midpoint(df: pd.DataFrame):
    # Calculate the midpoints
    df["xmid"] = (df["xmin"] + df["xmax"]) / 2
    df["ymid"] = (df["ymin"] + df["ymax"]) / 2

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


def snapshot_drop_parked(df_vehicle_snapshot: pd.DataFrame, windows: int = 5):
    indices_to_drop = []
    previous_row = None

    df_vehicle_snapshot = df_vehicle_snapshot.sort_values(by=["plate_number", "timestamp_precise"])
    for index, row in df_vehicle_snapshot.iterrows():
        if previous_row is not None:
            # Check if the plate_number is the same
            if row["plate_number"] == previous_row["plate_number"]:
                time_diff = row["timestamp_precise"] - previous_row["timestamp_precise"]
                if time_diff < timedelta(minutes=windows):
                    indices_to_drop.append(index)
        previous_row = row

    indices_to_drop.pop()
    df_vehicle_snapshot = df_vehicle_snapshot.drop(indices_to_drop)

    return df_vehicle_snapshot

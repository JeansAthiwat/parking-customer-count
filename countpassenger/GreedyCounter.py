from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import numpy as np
import os.path as osp
import os

PARKED_CHECK_WINDOW = 120


def match_cross_to_vehicle(df_cross, df_vehicle, start_padding: np.int64 = 5, stop_padding: np.int64 = 5):

    df_vehicle_copy = df_vehicle.copy()
    df_vehicle_copy["cross_count"] = 0

    for index, row in df_cross.iterrows():
        # Find the rows in df_vehicle where the timestamp is within the range
        mask_time = (df_vehicle_copy["timestamp_unix"] - start_padding <= row["timestamp_unix"]) & (
            df_vehicle_copy["timestamp_unix_end"] + stop_padding >= row["timestamp_unix"]
        )

        # if lifetime is more than 400sec it might be parking car check only the first 2 min and last 2 min
        mask_parked = (df_vehicle_copy["lifetime"] < 400) | (
            (row["timestamp_unix"] <= df_vehicle_copy["timestamp_unix"] + PARKED_CHECK_WINDOW)
            | (df_vehicle_copy["timestamp_unix_end"] - PARKED_CHECK_WINDOW <= row["timestamp_unix"])
        )

        vehicle_rows = df_vehicle_copy[mask_time & mask_parked]
        if vehicle_rows.empty:
            # print('empty mask')
            continue

        # Calculate the distance from the current cross to each vehicle
        distances = np.sqrt(
            (vehicle_rows["xmax"] - row["xmax"]) ** 2 + (vehicle_rows["ymax"] - row["ymax"]) ** 2
        )

        # Increment the cross count and mark as used for the nearest vehicle
        nearest_index = distances.idxmin(axis=0)
        df_vehicle_copy.loc[nearest_index, "cross_count"] += 1

    return df_vehicle_copy


def match_reverse_to_vehicle(df_reverse, df_vehicle, start_padding: int = 5, stop_padding: int = 5):

    df_vehicle_copy = df_vehicle.copy()
    df_vehicle_copy["reverse_count"] = 0

    # Iterate over each row in df_reverse
    for index, row in df_reverse.iterrows():
        # Find the rows in df_vehicle where the timestamp is within the range
        # print(row)
        mask_time = (df_vehicle_copy["timestamp_unix"] - start_padding <= row["timestamp_unix"]) & (
            df_vehicle_copy["timestamp_unix_end"] + stop_padding >= row["timestamp_unix"]
        )

        mask_parked = (df_vehicle_copy["lifetime"] < 400) | (
            (row["timestamp_unix"] <= df_vehicle_copy["timestamp_unix"] + PARKED_CHECK_WINDOW)
            | (df_vehicle_copy["timestamp_unix_end"] - PARKED_CHECK_WINDOW <= row["timestamp_unix"])
        )

        vehicle_rows = df_vehicle_copy[mask_time & mask_parked]
        if vehicle_rows.empty:
            # print('empty mask')
            continue

        # Calculate the distance from the current cross to each vehicle
        distances = np.sqrt(
            (vehicle_rows["xmax"] - row["xmax"]) ** 2 + (vehicle_rows["ymax"] - row["ymax"]) ** 2
        )
        # # Find the index of the nearest vehicle
        nearest_index = distances.idxmin(axis=0)
        df_vehicle_copy.loc[nearest_index, "reverse_count"] += 1

    return df_vehicle_copy


def predict_count(df_vehicle_processed, df_cross_processed, df_reverse_processed):
    vehicle_with_reverse_count = match_reverse_to_vehicle(df_reverse_processed, df_vehicle_processed)
    vehicle_with_cross_and_reverse = match_cross_to_vehicle(df_cross_processed, vehicle_with_reverse_count)
    return vehicle_with_cross_and_reverse

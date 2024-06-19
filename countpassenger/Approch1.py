from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import numpy as np
import os.path as osp
import os


def match_cross_to_vehicle(df_cross, df_vehicle, start_padding: int = 5, stop_padding: int = 20):

    df_vehicle_copy = df_vehicle.copy()
    df_vehicle_copy["cross_count"] = 0

    # Iterate over each row in df_cross
    for index, row in df_cross.iterrows():
        # Find the rows in df_vehicle where the timestamp is within the range
        mask = (df_vehicle_copy["timestamp_unix"] - start_padding <= row["timestamp_unix"]) & (
            df_vehicle_copy["timestamp_unix_end"] + stop_padding >= row["timestamp_unix"]
        )
        vehicle_rows = df_vehicle_copy[mask]
        if vehicle_rows.empty:
            # print('empty mask')
            continue

        # Calculate the distance from the current cross to each vehicle
        distances = np.sqrt(
            (vehicle_rows["xmax"] - row["xmin"]) ** 2 + (vehicle_rows["ymax"] - row["ymax"]) ** 2
        )
        # # Find the index of the nearest vehicle
        nearest_index = distances.idxmin(axis=0)

        # Increment the cross count and mark as used for the nearest vehicle
        df_vehicle_copy.loc[nearest_index, "cross_count"] += 1

    return df_vehicle_copy


def match_reverse_to_vehicle(
    df_reverse, df_vehicle, start_padding: int = 20, stop_padding: int = 5
):

    df_vehicle_copy = df_vehicle.copy()
    df_vehicle_copy["reverse_count"] = 0

    # Iterate over each row in df_reverse
    for index, row in df_reverse.iterrows():
        # Find the rows in df_vehicle where the timestamp is within the range
        # print(row)
        mask = (df_vehicle_copy["timestamp_unix"] - start_padding <= row["timestamp_unix"]) & (
            df_vehicle_copy["timestamp_unix_end"] + stop_padding >= row["timestamp_unix"]
        )
        vehicle_rows = df_vehicle_copy[mask]
        if vehicle_rows.empty:
            # print('empty mask')
            continue

        # Calculate the distance from the current cross to each vehicle
        distances = np.sqrt(
            (vehicle_rows["xmax"] - row["xmin"]) ** 2 + (vehicle_rows["ymax"] - row["ymax"]) ** 2
        )
        # # Find the index of the nearest vehicle
        nearest_index = distances.idxmin(axis=0)

        # Increment the cross count and mark as used for the nearest vehicle
        df_vehicle_copy.loc[nearest_index, "reverse_count"] += 1

    return df_vehicle_copy

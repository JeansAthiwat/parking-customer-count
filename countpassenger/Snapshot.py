from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import numpy as np
import os.path as osp
import os

CAPTURE_WINDOWS = 60  # seconds


def match_cross_cluster_snapshot_to_vehicle(
    df_vehicle_snapshot: pd.DataFrame, cluster_cross: pd.DataFrame, capture_window: int = CAPTURE_WINDOWS
) -> pd.DataFrame:

    df_vehicle_snapshot["cluster_cross_list"] = [[] for _ in range(len(df_vehicle_snapshot))]
    df_vehicle_snapshot["cross_count"] = 0

    for index, row in cluster_cross.iterrows():
        if row["cluster_id"] == -1:
            continue
        # Find the rows in df_vehicle where the timestamp is within the range
        mask = (row["timestamp_unix_min"] - capture_window <= df_vehicle_snapshot["timestamp_unix"]) & (
            df_vehicle_snapshot["timestamp_unix"] <= row["timestamp_unix_max"] + capture_window
        )
        vehicle_rows = df_vehicle_snapshot[mask]
        if vehicle_rows.empty:
            # print('no relevant vehicle to assign cluster')
            continue

        distances = np.sqrt(
            (vehicle_rows["xmid"] - row["xmid_mean"]) ** 2 + (vehicle_rows["xmid"] - row["ymid_mean"]) ** 2
        )

        # Increment the cross count and mark as used for the nearest vehicle
        nearest_index = distances.idxmin(axis=0)
        df_vehicle_snapshot.loc[nearest_index, "cluster_cross_list"].append(row["cluster_id"])
        df_vehicle_snapshot.loc[nearest_index, "cross_count"] += row["count"]

    return df_vehicle_snapshot


def match_reverse_cluster_snapshot_to_vehicle(
    df_vehicle_snapshot: pd.DataFrame, cluster_reverse: pd.DataFrame, capture_window: int = CAPTURE_WINDOWS
) -> pd.DataFrame:

    df_vehicle_snapshot["cluster_reverse_list"] = [[] for _ in range(len(df_vehicle_snapshot))]
    df_vehicle_snapshot["reverse_count"] = 0

    ###
    for index, row in cluster_reverse.iterrows():
        if row["cluster_id"] == -1:
            continue
        # Find the rows in df_vehicle where the timestamp is within the range
        mask = (row["timestamp_unix_min"] - capture_window <= df_vehicle_snapshot["timestamp_unix"]) & (
            df_vehicle_snapshot["timestamp_unix"] <= row["timestamp_unix_max"] + capture_window
        )
        vehicle_rows = df_vehicle_snapshot[mask]
        if vehicle_rows.empty:
            # print('no relevant vehicle to assign cluster')
            continue

        distances = np.sqrt(
            (vehicle_rows["xmid"] - row["xmid_mean"]) ** 2 + (vehicle_rows["xmid"] - row["ymid_mean"]) ** 2
        )

        # Increment the reverse count and mark as used for the nearest vehicle
        nearest_index = distances.idxmin(axis=0)
        df_vehicle_snapshot.loc[nearest_index, "cluster_reverse_list"].append(row["cluster_id"])
        df_vehicle_snapshot.loc[nearest_index, "reverse_count"] += row["count"]

    return df_vehicle_snapshot


def merge_same_car_snapshot(df_vehicle_snapshot: pd.DataFrame):
    # leave only the first row of that periods if df_vehicle_snapshot['plate_number'] are the same and the df_vehicle_snapshot['timestamp_precise'] diff is less than 5 minute
    return

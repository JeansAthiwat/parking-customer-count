from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import numpy as np
import os.path as osp
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import HDBSCAN

TIME_BIASED = 10
SPACE_BIASED = 800


def time_biased_distance2(point1, point2):
    """if the customer detected at the same time they might might be 2 cars. must increase penalty for coordinate"""
    # Apply quadratic bias to spatial distance
    spatial_distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    if spatial_distance < SPACE_BIASED:
        spatial_distance = 2 ** (spatial_distance / (SPACE_BIASED / 1.1))
    # Quadratic distance for time difference
    time_difference = np.abs(point1[2] - point2[2])
    if time_difference > TIME_BIASED:
        time_distance = time_difference**2
        return spatial_distance + time_distance
    else:
        time_distance = time_difference * 0.2
        return spatial_distance * 2 + time_distance

    # Combine the distances
    return spatial_distance + time_distance


def time_biased_distance1(point1, point2):
    # Apply quadratic bias to spatial distance
    spatial_distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    if spatial_distance < SPACE_BIASED:
        spatial_distance = 2 ** (spatial_distance / (SPACE_BIASED / 1.1))
    # Quadratic distance for time difference
    time_difference = np.abs(point1[2] - point2[2])
    if time_difference > TIME_BIASED:
        time_distance = time_difference**2
    else:
        time_distance = time_difference * 0.2

    # Combine the distances
    return spatial_distance + time_distance


def perform_cross_clustering(df_cross: pd.DataFrame, params: dict = conf.HDBSCAN_PARAMS):

    # ################ WHY? ###########
    # scaler_xy = StandardScaler()
    # df_cross[["xmid_std", "ymid_std"]] = scaler_xy.fit_transform(df_cross[["xmid", "ymid"]])
    # scaler_time = StandardScaler()
    # df_cross[["timestamp_unix_std"]] = scaler_time.fit_transform(df_cross[["timestamp_unix"]])
    # data = df_cross[["xmid_std", "ymid_std", "timestamp_unix_std"]].values
    # #################################

    data = df_cross[["xmid", "ymid", "timestamp_unix"]].values
    clusterer = HDBSCAN(**conf.HDBSCAN_PARAMS, metric=time_biased_distance2)  # Apply HDBSCAN
    clusters = clusterer.fit_predict(data)
    df_cross["cluster"] = clusters
    cluster_cross = create_cluster_df([(x, y, t, res) for (x, y, t), res in zip(data, clusters)])

    return df_cross, cluster_cross


def create_cluster_df(data):

    # Convert to pandas DataFrame
    df = pd.DataFrame(data, columns=["xmid", "ymid", "timestamp_unix", "cluster"])

    # Group by cluster and calculate min, max, and mean for each group
    grouped = (
        df.groupby("cluster")
        .agg(
            xmid_min=("xmid", "min"),
            xmid_max=("xmid", "max"),
            xmid_mean=("xmid", "mean"),
            ymid_min=("ymid", "min"),
            ymid_max=("ymid", "max"),
            ymid_mean=("ymid", "mean"),
            timestamp_unix_min=("timestamp_unix", "min"),
            timestamp_unix_max=("timestamp_unix", "max"),
            timestamp_unix_mean=("timestamp_unix", "mean"),
            count=("cluster", "count"),
        )
        .reset_index()
    )

    df_cluster = grouped.rename(columns={"cluster": "cluster_id"})
    return df_cluster


def assign_cluster_to_vehicle(
    df_vehicle: pd.DataFrame, cluster_cross: pd.DataFrame
) -> pd.DataFrame:
    # Ensure 'cluster_list' and 'count' columns exist in df_vehicle
    df_vehicle["cluster_list"] = [[] for _ in range(len(df_vehicle))]
    df_vehicle["count"] = 0

    for _, cluster_row in cluster_cross.iterrows():
        cluster_id = cluster_row["cluster_id"]
        timestamp_min = cluster_row["timestamp_unix_min"]
        timestamp_max = cluster_row["timestamp_unix_max"]
        cluster_count = cluster_row["count"]

        # Find all df_vehicle rows with timestamp_unix within the range
        # TODO:  df_vehicle["timestamp_unix"] <= timestamp_min
        mask = (df_vehicle["timestamp_unix"] >= timestamp_min) & (
            df_vehicle["timestamp_unix"] <= timestamp_max
        )
        matching_indices = df_vehicle.index[mask].tolist()

        if len(matching_indices) > 1:
            # Multiple matches: find the nearest based on (xmid, ymid) distance
            distances = [
                np.sqrt(
                    (df_vehicle.loc[i, "xmid"] - cluster_row["xmid_mean"]) ** 2
                    + (df_vehicle.loc[i, "ymid"] - cluster_row["ymid_mean"]) ** 2
                )
                for i in matching_indices
            ]
            nearest_index = matching_indices[np.argmin(distances)]
            df_vehicle.at[nearest_index, "cluster_list"].append(cluster_id)
            df_vehicle.at[nearest_index, "count"] += cluster_count

        elif len(matching_indices) == 1:
            # Single match: directly assign
            index = matching_indices[0]
            df_vehicle.at[index, "cluster_list"].append(cluster_id)
            df_vehicle.at[index, "count"] += cluster_count

        else:
            # No match: assign to the first df_vehicle where timestamp_unix is more than timestamp_max
            future_mask = df_vehicle["timestamp_unix"] > timestamp_max
            future_indices = df_vehicle.index[future_mask].tolist()

            if future_indices:
                index = future_indices[0]
                df_vehicle.at[index, "cluster_list"].append(cluster_id)
                df_vehicle.at[index, "count"] += cluster_count

    return df_vehicle

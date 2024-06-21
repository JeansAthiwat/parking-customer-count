from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import numpy as np
import os.path as osp
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import HDBSCAN

TIME_BIASED = 7
SPACE_BIASED = 800

PAD_END = 4


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


def time_biased_distance3(point1, point2):
    spatial_distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    time_difference = np.abs(point1[2] - point2[2])
    if time_difference < TIME_BIASED:
        time_difference = time_difference * 0.5
    else:
        time_difference = min(9999999, time_difference**2)

    return spatial_distance + time_difference * 10


def time_biased_distance1(point1, point2):
    spatial_distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    time_difference = np.abs(point1[2] - point2[2])

    return spatial_distance + time_difference


def smooth_transition(x, n=TIME_BIASED, k=1000):
    """Smooth transition function from linear to exponential behavior."""
    sigmoid = 1 / (1 + np.exp(-k * (x - n)))
    linear_part = x
    exponential_part = np.exp(x - n) + n - 1
    return linear_part * (1 - sigmoid) + exponential_part * sigmoid


def time_biased_distance4(point1, point2):
    spatial_distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    time_difference = np.abs(point1[2] - point2[2])
    time_distance = smooth_transition(time_difference)

    return spatial_distance * 0.1 + time_distance


def perform_cross_clustering(df_cross: pd.DataFrame, params: dict = conf.HDBSCAN_PARAMS):

    data = df_cross[["xmid", "ymid", "timestamp_unix"]].values
    clusterer = HDBSCAN(**params, metric=time_biased_distance4)
    clusters = clusterer.fit_predict(data)
    df_cross["cluster"] = clusters
    cluster_cross = create_cluster_df([(x, y, t, res) for (x, y, t), res in zip(data, clusters)])

    return df_cross, cluster_cross


def perform_reverse_clustering(df_reverse: pd.DataFrame, params: dict = conf.HDBSCAN_PARAMS):

    data = df_reverse[["xmid", "ymid", "timestamp_unix"]].values
    clusterer = HDBSCAN(**params, metric=time_biased_distance4)
    clusters = clusterer.fit_predict(data)
    df_reverse["cluster"] = clusters
    cluster_reverse = create_cluster_df([(x, y, t, res) for (x, y, t), res in zip(data, clusters)])

    return df_reverse, cluster_reverse


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

    df_cluster["timestamp_min"] = pd.to_datetime(df_cluster["timestamp_unix_min"], unit="s").dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    df_cluster["timestamp_max"] = pd.to_datetime(df_cluster["timestamp_unix_max"], unit="s").dt.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return df_cluster


def assign_cross_cluster_to_vehicle_in_lifetime(
    df_vehicle: pd.DataFrame, cluster_cross: pd.DataFrame, distance_metric: str = "cosim"
) -> pd.DataFrame:

    df_vehicle["cluster_cross_list"] = [[] for _ in range(len(df_vehicle))]
    df_vehicle["count_cross"] = 0

    # Extract relevant columns for faster access
    cluster_timestamps_min = cluster_cross["timestamp_unix_min"].values
    cluster_timestamps_max = cluster_cross["timestamp_unix_max"].values
    cluster_timestamps_mean = cluster_cross["timestamp_unix_mean"].values
    cluster_xmid_mean = cluster_cross["xmid_mean"].values
    cluster_ymid_mean = cluster_cross["ymid_mean"].values
    cluster_ids = cluster_cross["cluster_id"].values
    cluster_counts = cluster_cross["count"].values

    # Iterate over each vehicle
    for i, vehicle in df_vehicle.iterrows():
        # Boolean mask for clusters within the vehicle's lifetime
        in_lifetime_mask = (cluster_timestamps_mean >= vehicle["timestamp_unix"]) & (
            cluster_timestamps_mean <= vehicle["timestamp_unix_end"] + 6
        )

        # Filter clusters within the vehicle's lifetime
        relevant_clusters_xmid = cluster_xmid_mean[in_lifetime_mask]
        relevant_clusters_ymid = cluster_ymid_mean[in_lifetime_mask]
        relevant_cluster_ids = cluster_ids[in_lifetime_mask]
        relevant_cluster_counts = cluster_counts[in_lifetime_mask]

        # Direct assignment if only one cluster is within the lifetime
        if len(relevant_cluster_ids) == 1:
            df_vehicle.at[i, "cluster_cross_list"] = list(relevant_cluster_ids)
            df_vehicle.at[i, "count_cross"] = relevant_cluster_counts[0]
        else:
            if distance_metric == "euclidean":
                # Calculate Euclidean distances
                distances = np.sqrt(
                    (relevant_clusters_xmid - vehicle["xmid"]) ** 2
                    + (relevant_clusters_ymid - vehicle["ymid"]) ** 2
                )
                # Mask for clusters within the distance threshold
                within_distance_mask = distances < 700
            elif distance_metric == "cosim":
                # Calculate cosine similarity
                dot_products = (
                    relevant_clusters_xmid * vehicle["xmid"] + relevant_clusters_ymid * vehicle["ymid"]
                )
                magnitudes = np.sqrt(relevant_clusters_xmid**2 + relevant_clusters_ymid**2) * np.sqrt(
                    vehicle["xmid"] ** 2 + vehicle["ymid"] ** 2
                )
                cosine_similarities = dot_products / magnitudes
                # Mask for clusters with high cosine similarity
                within_distance_mask = cosine_similarities > 0.93

            # Assign clusters and counts to the vehicle
            df_vehicle.at[i, "cluster_cross_list"] = list(relevant_cluster_ids[within_distance_mask])
            df_vehicle.at[i, "count_cross"] = np.sum(relevant_cluster_counts[within_distance_mask])

    return df_vehicle


def assign_reverse_cluster_to_vehicle_in_lifetime(
    df_vehicle: pd.DataFrame, cluster_reverse: pd.DataFrame, distance_metric: str = "cosim"
) -> pd.DataFrame:

    df_vehicle["cluster_reverse_list"] = [[] for _ in range(len(df_vehicle))]
    df_vehicle["count_reverse"] = 0

    # Extract relevant columns for faster access
    cluster_timestamps_min = cluster_reverse["timestamp_unix_min"].values
    cluster_timestamps_max = cluster_reverse["timestamp_unix_max"].values
    cluster_xmid_mean = cluster_reverse["xmid_mean"].values
    cluster_ymid_mean = cluster_reverse["ymid_mean"].values
    cluster_ids = cluster_reverse["cluster_id"].values
    cluster_counts = cluster_reverse["count"].values

    # Iterate over each vehicle
    for i, vehicle in df_vehicle.iterrows():
        # Boolean mask for clusters within the vehicle's lifetime
        in_lifetime_mask = (vehicle["timestamp_unix"] - 5 <= cluster_timestamps_min) & (
            cluster_timestamps_max <= vehicle["timestamp_unix_end"]
        )

        # Filter clusters within the vehicle's lifetime
        relevant_clusters_xmid = cluster_xmid_mean[in_lifetime_mask]
        relevant_clusters_ymid = cluster_ymid_mean[in_lifetime_mask]
        relevant_cluster_ids = cluster_ids[in_lifetime_mask]
        relevant_cluster_counts = cluster_counts[in_lifetime_mask]

        # Direct assignment if only one cluster is within the lifetime
        if len(relevant_cluster_ids) == 1:
            df_vehicle.at[i, "cluster_reverse_list"] = list(relevant_cluster_ids)
            df_vehicle.at[i, "count_reverse"] = relevant_cluster_counts[0]
        else:
            if distance_metric == "euclidean":
                # Calculate Euclidean distances
                distances = np.sqrt(
                    (relevant_clusters_xmid - vehicle["xmid"]) ** 2
                    + (relevant_clusters_ymid - vehicle["ymid"]) ** 2
                )
                # Mask for clusters within the distance threshold
                within_distance_mask = distances < 700
            elif distance_metric == "cosim":
                # Calculate cosine similarity
                dot_products = (
                    relevant_clusters_xmid * vehicle["xmid"] + relevant_clusters_ymid * vehicle["ymid"]
                )
                magnitudes = np.sqrt(relevant_clusters_xmid**2 + relevant_clusters_ymid**2) * np.sqrt(
                    vehicle["xmid"] ** 2 + vehicle["ymid"] ** 2
                )
                cosine_similarities = dot_products / magnitudes
                # Mask for clusters with high cosine similarity
                within_distance_mask = cosine_similarities > 0.90

            # Assign clusters and counts to the vehicle
            df_vehicle.at[i, "cluster_reverse_list"] = list(relevant_cluster_ids[within_distance_mask])
            df_vehicle.at[i, "count_reverse"] = np.sum(relevant_cluster_counts[within_distance_mask])

    return df_vehicle

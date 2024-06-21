from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import numpy as np
import os.path as osp
import os


def match_cross_cluster_snapshot_to_vehicle(
    df_vehicle_snapshot: pd.DataFrame, cluster_cross: pd.DataFrame, distance_metric: str = "euclidean"
) -> pd.DataFrame:

    df_vehicle_snapshot["cluster_cross_list"] = [[] for _ in range(len(df_vehicle_snapshot))]
    df_vehicle_snapshot["count_cross"] = 0

    # Extract relevant columns for faster access
    cluster_timestamps_min = cluster_cross["timestamp_unix_min"].values
    cluster_timestamps_max = cluster_cross["timestamp_unix_max"].values
    cluster_timestamps_mean = cluster_cross["timestamp_unix_mean"].values
    cluster_xmid_mean = cluster_cross["xmid_mean"].values
    cluster_ymid_mean = cluster_cross["ymid_mean"].values
    cluster_ids = cluster_cross["cluster_id"].values
    cluster_counts = cluster_cross["count"].values

    # Iterate over each vehicle
    for i, vehicle in df_vehicle_snapshot.iterrows():
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
            df_vehicle_snapshot.at[i, "cluster_cross_list"] = list(relevant_cluster_ids)
            df_vehicle_snapshot.at[i, "count_cross"] = relevant_cluster_counts[0]
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
            df_vehicle_snapshot.at[i, "cluster_cross_list"] = list(
                relevant_cluster_ids[within_distance_mask]
            )
            df_vehicle_snapshot.at[i, "count_cross"] = np.sum(
                relevant_cluster_counts[within_distance_mask]
            )

    return df_vehicle_snapshot

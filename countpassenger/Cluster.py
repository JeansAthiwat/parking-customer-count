from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import numpy as np
import os.path as osp
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import HDBSCAN

TIME_BIASED = 15
SPACE_BIASED = 800


def time_biased_distance(point1, point2):
    # Apply quadratic bias to spatial distance
    spatial_distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
    if spatial_distance < SPACE_BIASED:
        spatial_distance = 2 ** (spatial_distance / (SPACE_BIASED / 1.1))
    # Quadratic distance for time difference
    time_difference = np.abs(point1[2] - point2[2])
    if time_difference > TIME_BIASED:
        time_distance = time_difference**2
    else:
        time_distance = time_difference * 0.1

    # Combine the distances
    return spatial_distance + time_distance


def perform_cross_clustering(df_cross: pd.DataFrame, params: dict = conf.HDBSCAN_PARAMS):
    cluster_cross = None

    # ################ WHY? ###########
    # # Normalize the x and y coordinates
    # scaler_xy = StandardScaler()
    # df_cross[["xmid_std", "ymid_std"]] = scaler_xy.fit_transform(df_cross[["xmid", "ymid"]])

    # # Normalize the timestamp_unix values
    # scaler_time = StandardScaler()
    # df_cross[["timestamp_unix_std"]] = scaler_time.fit_transform(df_cross[["timestamp_unix"]])
    # #################################
    # # Create a 3D array combining x, y, and timestamp_unix
    # data = df_cross[["xmid_std", "ymid_std", "timestamp_unix_std"]].values
    data = df_cross[["xmid", "ymid", "timestamp_unix"]].values

    # Define the HDBSCAN clustering algorithm

    clusterer = HDBSCAN(**conf.HDBSCAN_PARAMS, metric=time_biased_distance)  # Apply HDBSCAN
    df_cross["cluster"] = clusterer.fit_predict(data)
    # print(df_cross[df_cross["cluster"] == -1].to_string())

    return df_cross, cluster_cross

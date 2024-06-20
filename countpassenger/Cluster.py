from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import numpy as np
import os.path as osp
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import HDBSCAN


def perform_cross_clustering(df_cross: pd.DataFrame, params: dict = conf.HDBSCAN_PARAMS):
    cluster_cross = None

    ################ WHY? ###########
    # Normalize the x and y coordinates
    scaler_xy = StandardScaler()
    df_cross[["xmid_std", "ymid_std"]] = scaler_xy.fit_transform(df_cross[["xmid", "ymid"]])

    # Normalize the timestamp_unix values
    scaler_time = StandardScaler()
    df_cross[["timestamp_unix_std"]] = scaler_time.fit_transform(df_cross[["timestamp_unix"]])
    #################################
    # Create a 3D array combining x, y, and timestamp_unix
    data = df_cross[["xmid_std", "ymid_std", "timestamp_unix_std"]].values

    # Define the HDBSCAN clustering algorithm

    clusterer = HDBSCAN(**conf.HDBSCAN_PARAMS)  # Apply HDBSCAN
    df_cross["cluster"] = clusterer.fit_predict(data)
    # print(df_cross[df_cross["cluster"] == -1].to_string())

    return df_cross, cluster_cross

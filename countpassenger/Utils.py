from countpassenger.Config import conf
from countpassenger import Preprocess

import countpassenger
import pandas as pd
import numpy as np
import os.path as osp
import os

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import HDBSCAN


def print_range(df: pd.DataFrame, start: np.int64 = 1714284000, stop: np.int64 = 1714288000):
    print(df[(df["timestamp_unix"] >= start) & (df["timestamp_unix_end"] <= stop)].to_string())

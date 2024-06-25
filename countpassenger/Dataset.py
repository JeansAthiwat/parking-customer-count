import pandas as pd
import numpy as np
import os
import os.path as osp
from countpassenger.Config import conf


def load_dataset_from_paths(
    vehicle_path_rel: str,
    cross_path_rel: str,
    reverse_path_rel: str,
    day_relative: bool = True,
    raw_dir: str = conf.RESOURCES_RAW_DIR,
):
    if day_relative:
        df_vehicle = pd.read_csv(osp.join(raw_dir, vehicle_path_rel))
        df_cross = pd.read_csv(osp.join(raw_dir, cross_path_rel))
        df_reverse = pd.read_csv(osp.join(raw_dir, reverse_path_rel))
    else:
        df_vehicle = pd.read_csv(raw_dir, vehicle_path_rel)
        df_cross = pd.read_csv(raw_dir, cross_path_rel)
        df_reverse = pd.read_csv(raw_dir, reverse_path_rel)
    return df_vehicle, df_cross, df_reverse

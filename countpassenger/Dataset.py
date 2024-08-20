import pandas as pd
import numpy as np
import os
import os.path as osp
from countpassenger.Config import conf


def load_dataset_from_paths(
    vehicle_csv_path: str,
    cross_csv_path: str,
    reverse_csv_path: str,
    path_day_relative: bool = False,
    raw_dir: str = conf.RESOURCES_RAW_DIR,
):
    if path_day_relative:
        df_vehicle = pd.read_csv(osp.join(raw_dir, vehicle_csv_path))
        df_cross = pd.read_csv(osp.join(raw_dir, cross_csv_path))
        df_reverse = pd.read_csv(osp.join(raw_dir, reverse_csv_path))
    else:
        df_vehicle = pd.read_csv(vehicle_csv_path)
        df_cross = pd.read_csv(cross_csv_path)
        df_reverse = pd.read_csv(reverse_csv_path)

    return df_vehicle, df_cross, df_reverse

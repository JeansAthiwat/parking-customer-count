import os
import os.path as osp
import math

_TIME_BIAS = 6


class Config:

    def __init__(self, *args, **kwargs):

        self.BASE_DIR = "/home/jeans/internship/parking-customer-count"
        self.RESOURCES_DIR = osp.join(self.BASE_DIR, "resources")
        self.RESOURCES_RAW_DIR = osp.join(self.RESOURCES_DIR, "raw")
        self.RESOURCES_PROCESSED_DIR = osp.join(self.RESOURCES_DIR, "processed")

        # HDBSCAN
        # TODO: tune these
        self.HDBSCAN_PARAMS = dict(
            min_cluster_size=2,
            min_samples=None,
            cluster_selection_epsilon=0,  # math.sqrt(1440**2 + 2560**2) + _TIME_BIAS,
            max_cluster_size=40,
            # specify yourown
            # metric="euclidean",
            # metric_params=None,
            alpha=1.0,
            algorithm="brute",
            leaf_size=1000,
            n_jobs=None,
            cluster_selection_method="leaf",
            allow_single_cluster=False,
            store_centers="medoid",
            copy=False,
        )

        self.VEHICLE_INTEREST_NON_SNAPSHOT = [
            "camera",
            "timestamp_precise",
            "lifetime",
            "xmid",
            "ymid",
            "plate_number",
            # "similarized_plate_number",
            "vehicle_type",
            # "vehicle_type_confidence",
            "timestamp_unix",
            "timestamp_unix_end",
        ]

        self.VEHICLE_INTEREST_SNAPSHOT = [
            "camera",
            "timestamp_precise",
            "xmid",
            "ymid",
            "lifetime",
            "plate_number",
            # "similarized_plate_number",
            "vehicle_type",
            # "vehicle_type_confidence",
            "timestamp_unix",
            "timestamp_unix_end",
        ]

        self.CUSTOMER_INTEREST_SNAPSHOT = [
            "camera",
            "timestamp_precise",
            "xmid",
            "ymid",
        ]

        self.CLUSTER_INTEREST = [
            "timestamp_min",
            "timestamp_max",
            "count",
            "cluster_id",
            "xmid_mean",
            "ymid_mean",
        ]

        self.VEHICLE_INTEREST_NON_SNAPSHOT_CLUSTERED = [
            "camera",
            "timestamp_precise",
            "lifetime",
            "xmid",
            "ymid",
            "plate_number",
            # "similarized_plate_number",
            "vehicle_type",
            # "vehicle_type_confidence",
            "timestamp_unix",
            "timestamp_unix_end",
            "count",
            "cluster_list",
        ]


conf = Config()

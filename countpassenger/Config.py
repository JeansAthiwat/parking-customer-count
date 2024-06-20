import os
import os.path as osp


class Config:

    def __init__(self, *args, **kwargs):

        self.BASE_DIR = "/home/jeans/internship/parking-customer-count"
        self.RESOURCES_DIR = osp.join(self.BASE_DIR, "resources")
        self.RESOURCES_RAW_DIR = osp.join(self.RESOURCES_DIR, "raw")
        self.RESOURCES_PROCESSED_DIR = osp.join(self.RESOURCES_DIR, "processed")

        # HDBSCAN
        self.HDBSCAN_PARAMS = dict(
            min_cluster_size=2,
            min_samples=None,
            cluster_selection_epsilon=0.0,
            max_cluster_size=50,
            metric="euclidean",
            metric_params=None,
            alpha=1.0,
            algorithm="auto",
            leaf_size=40,
            n_jobs=None,
            cluster_selection_method="eom",
            allow_single_cluster=False,
            store_centers=None,
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
            "xmin",
            "xmax",
            "ymin",
            "ymax",
        ]


conf = Config()

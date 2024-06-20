import os
import os.path as osp


class Config:

    def __init__(self, *args, **kwargs):

        self.BASE_DIR = "/home/jeans/internship/parking-customer-count"
        self.RESOURCES_DIR = osp.join(self.BASE_DIR, "resources")
        self.RESOURCES_RAW_DIR = osp.join(self.RESOURCES_DIR, "raw")
        self.RESOURCES_PROCESSED_DIR = osp.join(self.RESOURCES_DIR, "processed")

        # HDBSCAN
        self.HDBSCAN_MINIMUM_CLUSTER_SIZE = 2
        self.HDBSCAN_MAXIMUM_CLUSTER_SIZE = 50

        self.VEHICLE_INTEREST = [
            "timestamp_precise",
            "plate_number",
            "camera",
            "lifetime",
            "plate_number_confidence",
            "similarized_plate_number",
            "vehicle_type",
            "vehicle_type_confidence",
        ]

        self.VEHICLE_INTEREST_SNAPSHOT = [
            "camera",
            "timestamp_precise",
            "xmin",
            "xmax",
            # "ymin",
            "ymax",
            "lifetime",
            "plate_number",
            # "similarized_plate_number",
            "vehicle_type",
            # "vehicle_type_confidence",
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

from countpassenger.Config import conf
from countpassenger import Preprocess
from countpassenger.GreedyCounter import predict_count
from countpassenger.Postprocess import export_customer_count
from countpassenger import Dataset
import pandas as pd

# -----------------------------MAKE CHANGES HERE--------------------------#

# full path to the input csv files for vehicle, cross , and reverse in this order
VEHICLE_CSV_PATH = "/home/jeans/internship/parking-customer-count/resources/raw/2024-07-01/mbk-tourist-vehicle-object-20240701-20240731.csv"
CROSS_CSV_PATH = "/home/jeans/internship/parking-customer-count/resources/raw/2024-07-01/mbk-tourist-raw-cross-object-20240701-20240731.csv"
REVERSE_CSV_PATH = "/home/jeans/internship/parking-customer-count/resources/raw/2024-07-01/mbk-tourist-raw-reverse-object-20240701-20240731.csv"

output_folder = "./resources/processed"  # Folder the csv file will be exported to
output_file_name = "formatted_mbk_2024-07-01-test.csv"  # Exported csv file name


# all the camera name that appear on-site (in-case using with other places other than mbk)
CAMERA_LIST = ["mbk-14-11", "mbk-14-12", "mbk-14-13", "mbk-14-14"]

# ------------------------------------------------------------------------#

# load the dataset from directory path
df_vehicle_raw, df_cross_raw, df_reverse_raw = Dataset.load_dataset_from_paths(
    vehicle_csv_path=VEHICLE_CSV_PATH, cross_csv_path=CROSS_CSV_PATH, reverse_csv_path=REVERSE_CSV_PATH
)

vehicle_with_cross_and_reverse = pd.DataFrame()
for current_cam in CAMERA_LIST:

    # preprocess the data
    vehicle = Preprocess.df_clean_vehicle(df_vehicle_raw=df_vehicle_raw, current_camera=current_cam)
    cross = Preprocess.df_clean_customer(df_customer=df_cross_raw, current_cam=current_cam)
    reverse = Preprocess.df_clean_customer(df_customer=df_reverse_raw, current_cam=current_cam)

    vehicle_with_cross_and_reverse_tmp = predict_count(
        vehicle,
        cross,
        reverse,
    )

    print(
        f"process for cam:{current_cam} completed. total entry: {vehicle_with_cross_and_reverse_tmp.shape[0]}"
    )
    vehicle_with_cross_and_reverse = pd.concat(
        [vehicle_with_cross_and_reverse, vehicle_with_cross_and_reverse_tmp], ignore_index=True
    )

print(vehicle_with_cross_and_reverse.shape)

# Setting this to True, will drop the null vehicle_plate row (drop row ที่จับทะเบียนไม่ติด)
drop_null_cell = True

export_customer_count(
    vehicle_with_cross_and_reverse,
    output_file_name=output_file_name,
    output_folder=output_folder,
    drop_null_cell=drop_null_cell,
)

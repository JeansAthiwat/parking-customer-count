# HOW TO USE

1. เปิดไฟล์ "count_from_csv.py" แล้วแก้ parameter ดังนี้

    ### Important:
        - VEHICLE_CSV_PATH: Path pointing to the RAW vehicle-object .csv file.
        - CROSS_CSV_PATH: Path pointing to the RAW cross-object .csv file.
        - REVERSE_CSV_PATH: Path pointing to the RAW reverse-object .csv file.

        - output_folder: The directory (or folder) that the output file will be exported to. 
        - output_file_name: The name of the output file (should ends with .csv)

    ### Additional params (No need to change these)
    - CAMERA_LIST: list ของชื่อกล้องที่มี

    ### EXAMPLE
    ```.py
    # full path to the input csv files for vehicle, cross , and reverse in this order
    VEHICLE_CSV_PATH = "/home/jeans/internship/parking-customer-count/resources/raw/2024-07-01/mbk-tourist-vehicle-object-20240701-20240731.csv"
    CROSS_CSV_PATH = "/home/jeans/internship/parking-customer-count/resources/raw/2024-07-01/mbk-tourist-raw-cross-object-20240701-20240731.csv"
    REVERSE_CSV_PATH = "/home/jeans/internship/parking-customer-count/resources/raw/2024-07-01/mbk-tourist-raw-reverse-object-20240701-20240731.csv"

    output_folder = "./resources/processed"  # Folder the csv file will be exported to
    output_file_name = "formatted_mbk_2024-07-01-test.csv"  # Exported csv file name


    # all the camera name that appear on-site (in-case using with other places other than mbk)
    CAMERA_LIST = ["mbk-14-11", "mbk-14-12", "mbk-14-13", "mbk-14-14"]

    ```

2. กด run count_from_csv.py ได้เลย output จะอยู่ที่ "{output_folder}/{output_file_name}"
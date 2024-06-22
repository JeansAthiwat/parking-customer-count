import pandas as pd


def concatenate_csv(files, output_path):
    # Initialize an empty list to hold the dataframes
    dataframes = []

    # Iterate through the list of files and read each into a dataframe
    for file in files:
        try:
            df = pd.read_csv(file)
            dataframes.append(df)
            print(f"Successfully read {file}")
        except Exception as e:
            print(f"Error reading {file}: {e}")

    # Concatenate all the dataframes
    concatenated_df = pd.concat(dataframes, ignore_index=True)

    # Write the concatenated dataframe to a new CSV file
    concatenated_df.to_csv(output_path, index=False)
    print(f"Concatenated CSV written to {output_path}")


# # Example usage
# file_list = [
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29/count-passengers-mbk-14-11-vehicle-snapshot.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29/count-passengers-mbk-14-12-vehicle-snapshot.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29/count-passengers-mbk-14-13-vehicle-snapshot.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29/count-passengers-mbk-14-14-vehicle-snapshot.csv",
# ]
# output_file = "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29_count-passengers-mbk-tourist-vehicle-object-snapshot.csv"

# # Example usage
# file_list = [
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29/count-passengers-mbk-14-11-vehicle.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29/count-passengers-mbk-14-12-vehicle.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29/count-passengers-mbk-14-13-vehicle.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29/count-passengers-mbk-14-14-vehicle.csv",
# ]
# output_file = "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-29_count-passengers-mbk-tourist-vehicle-object.csv"

# # Example usage
# file_list = [
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28/count-passengers-mbk-14-11-vehicle-snapshot.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28/count-passengers-mbk-14-12-vehicle-snapshot.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28/count-passengers-mbk-14-13-vehicle-snapshot.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28/count-passengers-mbk-14-14-vehicle-snapshot.csv",
# ]
# output_file = "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28_count-passengers-mbk-tourist-vehicle-object-snapshot.csv"

# # Example usage
# file_list = [
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28/count-passengers-mbk-14-11-vehicle.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28/count-passengers-mbk-14-12-vehicle.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28/count-passengers-mbk-14-13-vehicle.csv",
#     "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28/count-passengers-mbk-14-14-vehicle.csv",
# ]
# output_file = "/home/jeans/internship/parking-customer-count/resources/processed/2024-04-28_count-passengers-mbk-tourist-vehicle-object.csv"


concatenate_csv(file_list, output_file)

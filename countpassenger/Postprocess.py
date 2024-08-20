import pandas as pd
import os


def export_customer_count(df_with_count, output_path, drop_null_cell=False, subset=["plate_number"]):
    """
    Filters specific columns from a CSV file and exports to a new CSV file.

    Parameters:
    input_path (str): Path to the input CSV file.
    output_path (str): Path to the output CSV file.
    """
    # Define the columns to be extracted
    columns_to_extract = [
        "timestamp_precise",
        "plate_number",
        "vehicle_type",
        "cross_count",
        "reverse_count",
    ]

    try:

        # Check if all necessary columns are present
        if all(col in df_with_count.columns for col in columns_to_extract):
            # Extract the specific columns
            filtered_df = df_with_count[columns_to_extract]
            if drop_null_cell:
                filtered_df = filtered_df.dropna(subset=subset)

            # Write the filtered dataframe to a new CSV file
            filtered_df.to_csv(output_path, index=False)
            print(f"Filtered CSV written to {output_path}")
        else:
            missing_columns = [col for col in columns_to_extract if col not in df_with_count.columns]
            print(f"Error: Missing columns in input file: {missing_columns}")

    except Exception as e:
        print(f"Error processing file: {e}")

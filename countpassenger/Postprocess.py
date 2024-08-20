import pandas as pd
import os

EXPORT_COLUMN_ORDER = [
    "timestamp_precise",
    "year",
    "month",
    "date",
    "hour",
    "plate_number",
    "vehicle_type",
    "exit",
    "entrance",
]
# Define the columns to be extracted
COLUMNS_TO_EXTRACT = [
    "timestamp_precise",
    "plate_number",
    "vehicle_type",
    "cross_count",
    "reverse_count",
]


def export_customer_count(
    df_with_count,
    output_file_name=None,
    output_folder="./",
    columns_to_extract=COLUMNS_TO_EXTRACT,
    drop_null_cell=True,
    subset=["plate_number"],
    apply_p_tung_format=True,
):
    """
    Filters specific columns from a CSV file and exports to a new CSV file.

    Parameters:
    input_path (str): Path to the input CSV file.
    output_path (str): Path to the output CSV file.
    """

    assert output_file_name, "No export file_name were given."

    if ".csv" not in output_file_name:
        output_file_name + ".csv"

    csv_path = os.path.join(output_folder, output_file_name)

    # Check if all necessary columns are present
    if not all(col in df_with_count.columns for col in columns_to_extract):
        missing_columns = [col for col in columns_to_extract if col not in df_with_count.columns]
        print(f"Error: Missing columns in input file: {missing_columns}")

    try:
        # Extract the specific columns
        filtered_df = df_with_count[columns_to_extract]

        if drop_null_cell:
            filtered_df = filtered_df.dropna(subset=subset)

        if apply_p_tung_format:
            filtered_df = p_tung_format(filtered_df, output_path=output_folder, file_name=output_file_name)

        # Write the filtered dataframe to a new CSV file
        filtered_df.to_csv(csv_path, index=False)
        print(f"formatted csv file saved at {csv_path}")
        print(f"total entry after dropping null rows: {filtered_df.shape[0]}")

    except Exception as e:
        print(f"Error processing file: {e}")


def extract_date(df, add_from_GMT=7, remove_millisec=True):
    # Extract year, month, day, and hour from the timestamp column

    # Add 7 hours to the timestamp column
    df["timestamp_precise"] = df["timestamp_precise"] + pd.Timedelta(hours=add_from_GMT)
    df["year"] = df["timestamp_precise"].dt.year
    df["month"] = df["timestamp_precise"].dt.month
    df["date"] = df["timestamp_precise"].dt.day
    df["hour"] = df["timestamp_precise"].dt.hour

    # Remove the decimal milliseconds from 'timestamp_precise'
    if remove_millisec:
        df["timestamp_precise"] = df["timestamp_precise"].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df


def p_tung_format(df, output_path, file_name=None, add_from_GMT=7, column_order=EXPORT_COLUMN_ORDER):

    # Ensure the timestamp column is in datetime format
    df["timestamp_precise"] = pd.to_datetime(df["timestamp_precise"])
    df = extract_date(df, add_from_GMT)

    # Rename the columns. "cross_count"   -> "exit". "reverse_count" -> "entrance"
    df = df.rename(columns={"cross_count": "exit", "reverse_count": "entrance"})
    # reorder columns
    df = df[column_order]
    return df

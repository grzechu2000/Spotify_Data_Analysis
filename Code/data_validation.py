import os
import pandas as pd

def is_csv_complete(file_path):
    try:
        df = pd.read_csv(file_path)

        # Check for missing values
        if df.isnull().values.any():
            return False
        else:
            return True

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

def validate_csv_files(directory_path):

    if not os.path.exists(directory_path):
        print(f"📁 Directory {directory_path} does not exist!")
        return

    for filename in os.listdir(directory_path):
        if filename.endswith(".csv"):
            file_path = os.path.join(directory_path, filename)
            is_complete = is_csv_complete(file_path)
            if not is_complete:
                print(f"❌ Empty cell in: {file_path}")
            else:
                print(f"✅ Passed completeness check for: {file_path}")

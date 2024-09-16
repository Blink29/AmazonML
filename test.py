import os

def count_files_in_folder(folder_path):
    try:
        # List all files and directories in the given folder
        files = os.listdir(folder_path)
        # Filter out directories, keep only files
        file_count = sum([1 for f in files if os.path.isfile(os.path.join(folder_path, f))])
        return file_count
    except Exception as e:
        print(f"Error: {e}")
        return 0

# Path to the folder
folder_path = 'testing_dataset'
num_files = count_files_in_folder(folder_path)
print(f"Number of files in '{folder_path}': {num_files}")

# import pandas as pd
# import os

# # Load your CSV file
# input_csv = 'dataset/train.csv'  # Replace with your actual file path
# df = pd.read_csv(input_csv)

# output_folder = 'split_dataset'
# os.makedirs(output_folder, exist_ok=True)

# # Group the rows by 'entity_name' column
# grouped = df.groupby('entity_name')  # Replace with the column you want to group by

# # Loop through each group and save to a separate CSV file
# for entity, group in grouped:
#     # Create a new CSV file for each entity
#     output_file = os.path.join(output_folder, f'{entity}_classified.csv')  # Replace with your preferred naming scheme
#     group.to_csv(output_file, index=False)
#     print(f'Created file: {output_file}')
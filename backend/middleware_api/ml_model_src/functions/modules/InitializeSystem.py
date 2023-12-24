import os

def create_directories():
    current_directory = os.path.dirname(__file__)
    parent_directory = os.path.dirname(current_directory)
    home_directory = os.path.dirname(parent_directory)

    storage_directory = os.path.join(home_directory, "storage")
    if not os.path.exists(storage_directory):
        os.makedirs(storage_directory)

    snapshots_directory = os.path.join(storage_directory, "snapshots")
    if not os.path.exists(snapshots_directory):
        os.makedirs(snapshots_directory)

    for filename in os.listdir(snapshots_directory):
        file_path = os.path.join(snapshots_directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")







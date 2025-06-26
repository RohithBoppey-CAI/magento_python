import os
import json


def save_as_file_local(base_dir: str = "./", file_name: str = "", data: dict = {}):
    if not base_dir:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    if bool(data): 
        print("Cannot save empty / non-valid response in a file, exiting.")
        return 
    
    # Create the directory recursively if it doesn't exist
    os.makedirs(base_dir, exist_ok=True)

    # Construct the full file path
    full_path = os.path.join(base_dir, file_name)
    print(f"Saving the file to: {full_path}")

    # Save the data as JSON
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return full_path

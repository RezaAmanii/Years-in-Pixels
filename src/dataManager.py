from pathlib import Path
from typing import Any
import json



class DataManager:
    """
    DataManager class for handling user data stored in a JSON file.
    This class is responsible for:
    - Loading user data from a file
    - Creating the file with default data if it does not exists
    - Updating (Saving) user data back to the file
    """

    def __init__(self, file_name, default_data):
        """
        Initialize the DataManager.

        Args:
            file_name (str): The name or path of the JSON file.
            default_data (dict): Default data to use if the file is missing or corrupted.
        """

        self.file_path = Path(file_name)
        self.default_data = default_data



    def load_users_data(self) -> dict[str, dict[str, Any]]:
        """
        Load_users_data function for loading user's data from the JSON file.

        Returns:
            dict[str, dict[str, Any]]: The loaded user data.

        """
        if self.file_path.exists():
            print(f"Loading user's data file ({self.file_path}).")
            with open(self.file_path, "r") as file:
                try:
                    return json.load(file)
                except json.JSONDecodeError:
                    print("Data file corrupted. Loading defaults.")
                    return self.default_data
        
        print(f"File: {self.file_path} not found. Creating a new one...")
        self.update_users_data(self.default_data)
        return self.default_data



    def update_users_data(self, user_data: dict) -> None:
        """
        update_suers_data function for saving/updating user's data to the JSON file.

        Args:
            user_data (dict): The user data to be saved.
        """
        with open(self.file_path, "w") as file:
            json.dump(user_data, file, indent=4)

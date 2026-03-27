import os
import json



class DataManager:
    def __init__(self, file_name, default_data):
        self.file_name = file_name
        self.default_data = default_data


    def load_users_data(self) -> dict[str, dict[str, str]]:
        if os.path.exists(self.file_name):
            print(f"Loading user's data file ({self.file_name}).")
            with open(self.file_name, "r") as file:
                user_data = json.load(file)
        else:
            print(
                f"File: {self.file_name} was not found in your directory. Creating a new one...")
            with open(self.file_name, "w") as file:
                file.write(json.dumps(self.default_data))
                user_data = self.default_data

        return user_data


    def update_users_data(self, user_data: dict[str, dict[str, str]]) -> None:
        if os.path.exists(self.file_name):
            with open(self.file_name, "w") as file:
                file.write(json.dumps(user_data))

        else:
            print(f"File: {self.file_name} was not found in your directory.")

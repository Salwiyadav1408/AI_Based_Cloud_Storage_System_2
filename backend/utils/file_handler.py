import os

def create_user_folders(email: str):
    folders = [
        f"storage/{email}/selfie",
        f"storage/{email}/non_selfie",
        f"storage/{email}/resume",
        f"storage/{email}/other"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)
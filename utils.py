import os
import requests

def download_file_from_google_drive(file_id, destination):
    """Downloads a file from Google Drive."""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url, stream=True)
    
    if response.status_code == 200:
        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print("Download complete.")
    else:
        print("Failed to download file. Check the file ID or permissions.")

def load_idx_file():
    """Downloads and loads the .idx file from Google Drive."""
    file_id = "1gm1ukBH_tAwApNOGju0ky4IyT9HdLtRy"  # Replace with your actual file ID
    destination = "data/faiss_hnsw_index.idx"  # Path to save the .idx file
    os.makedirs("data", exist_ok=True)  # Create the data directory if it doesn't exist

    if not os.path.exists(destination):
        print("Downloading .idx file from Google Drive...")
        download_file_from_google_drive(file_id, destination)

    return destination

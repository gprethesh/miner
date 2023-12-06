import os
import requests
from requests.exceptions import HTTPError
from tqdm import tqdm


def download_zip(url, jobid, file_hash):
    try:
        # Create 'job' directory if it doesn't exist
        job_folder_path = os.path.join(os.getcwd(), "job")
        os.makedirs(job_folder_path, exist_ok=True)

        # Create the directory for jobid within the 'job' folder
        folder_path = os.path.join(job_folder_path, jobid)
        os.makedirs(folder_path, exist_ok=True)

        # Use the file_hash as the file name, append .zip extension
        file_name = f"{file_hash}.zip"

        # Construct file path
        file_path = os.path.join(folder_path, file_name)

        # Check if file already exists
        if os.path.exists(file_path):
            raise FileExistsError(
                f"The file {file_name} already exists in the directory {folder_path}."
            )

        # Download the zip file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

        # Get total size in bytes.
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024  # 1 Kibibyte

        # Save the zip file
        with open(file_path, "wb") as file, tqdm(
            desc=file_name,
            total=total_size,
            unit="iB",
            unit_scale=True,
            unit_divisor=1024,
        ) as bar:
            for data in response.iter_content(block_size):
                bar.update(len(data))
                file.write(data)

        print(f"File downloaded successfully and saved as {file_path}")

        return True

    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except FileExistsError as file_err:
        print(file_err)
    except Exception as err:
        print(f"An error occurred: {err}")

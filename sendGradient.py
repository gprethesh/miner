import os
import json
from tqdm import tqdm
import asyncio
import config


async def send_file_via_websocket(websocket, file_path, message_type, just_name, fld):
    try:
        print("I'm being called")
        # Check if the file exists
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return

        # Extract folder name and file name
        folder_name = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)

        # Determine the file size for progress tracking
        file_size = os.path.getsize(file_path)

        # Create a message with type, folder name, and file name
        message = {
            "type": message_type,
            "folder_name": folder_name,
            "file_name": file_name,
            "file_data": None,  # Placeholder for chunks of file data
            "just_name": just_name,
            "job_name": fld,
            "wallet_address": config.WALLET_ADDRESS,
        }

        # Open and read the file in chunks
        with open(file_path, "rb") as file:
            print("Reading file")
            with tqdm(
                total=file_size, unit="B", unit_scale=True, desc="Sending File"
            ) as pbar:
                while True:
                    chunk = file.read(65536)  # Adjust the chunk size as needed #65536
                    if not chunk:
                        break  # End of file

                    message["file_data"] = chunk.decode("latin1")
                    await websocket.send(json.dumps(message))
                    pbar.update(len(chunk))

        # Send a final message indicating the end of the file transfer
        message["file_data"] = "EOF"
        await websocket.send(json.dumps(message))

        # Wait for a response
        response = await websocket.recv()
        return response

    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except OSError as e:
        print(f"Error opening file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

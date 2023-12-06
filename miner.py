import socket
import json
import config
import websockets
import asyncio

from train_and_contribute import train_and_contribute
from jobDownload import download_zip
from getJob import get_first_zip_in_job
from deleteJob import delete_jobid_folder_and_file
from getGradient import find_gradient
from sendGradient import send_file_via_websocket
from requestJob import request_job_file


class MessageType:
    GRADIENT = "gradient"
    REQUESTFILE = "requestFile"
    DOWNLOADFILE = "downloadFile"


async def ping_server(message_type, find_gradient, download_zip):
    uri = "ws://127.0.0.1:5500"
    try:
        async with websockets.connect(uri) as websocket:
            # Send a ping message
            await websocket.send("hello")

            # Wait for a response
            response = await websocket.recv()
            print("Received from server:", response)

            request_response = await request_job_file(
                websocket, MessageType.REQUESTFILE
            )
            print("Server response :", request_response)

            try:
                # Parse the JSON response into a Python dictionary
                response_data = json.loads(request_response)

                # Handle double encoded JSON
                if isinstance(response_data, str):
                    response_data = json.loads(response_data)

                if (
                    isinstance(response_data, dict)
                    and response_data.get("message_type") == MessageType.DOWNLOADFILE
                ):
                    url = response_data.get("url")
                    file_hash = response_data.get("file_hash")
                    jobname = response_data.get("active_mining_value")
                    value = download_zip(url, jobname, file_hash)

                    if value:
                        folder, zip_file, file_name = get_first_zip_in_job("job")
                        if folder and zip_file:
                            print(
                                f"Oldest folder: {folder}, First zip file: {zip_file}"
                            )
                            miner_id = file_name
                            path = f"./job/{folder}/{zip_file}"
                            miner_wallet_address = config.WALLET_ADDRESS
                            gradient = train_and_contribute(miner_id, path, folder)
                            print("Gradient", gradient)
                            delete_jobid_folder_and_file("job", folder, zip_file)
                        else:
                            print("No folder or zip file found to Train")
                else:
                    print("Error: Response data is not a valid JSON object.")

            except json.JSONDecodeError:
                print("Error: Could not decode JSON response.")
            except TypeError:
                print("TypeError: The response is not in the expected format.")
            except AttributeError:
                print("AttributeError: Unexpected data type.")

            fld, fil, just_name = find_gradient("Destination")
            if fld and fil:
                print(f"Oldest folder: {fld}, First .pth file: {fil}")
                file_path = f"./Destination/{fld}/{fil}"
                if message_type == MessageType.GRADIENT:
                    file_response = await send_file_via_websocket(
                        websocket, file_path, MessageType.GRADIENT, just_name, fld
                    )
                    print("Called to send the gradient")
                    print("Server response after file send:", file_response)
                    if file_response:
                        delete_jobid_folder_and_file("Destination", fld, fil)
                    else:
                        print("Gradient failed to be sent")
            else:
                print("No gradient file found to send.")

    except websockets.ConnectionClosedError:
        print("ConnectionClosedError: The websocket connection is closed unexpectedly.")
    except websockets.WebSocketException as e:
        print(
            f"WebSocketException: An error occurred with the websocket connection. Details: {e}"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


# Run the client


async def start_server(find_gradient, download_zip):
    print(" Starting Miner...")
    try:
        while True:
            try:
                await ping_server(MessageType.GRADIENT, find_gradient, download_zip)
            except Exception as e:
                print(" Miner closed due to an error:", e)
                break
            await asyncio.sleep(60)
    except KeyboardInterrupt:
        print(" Miner shutdown initiated by user.")
    finally:
        print(" Shutting down Miner...")


# Start the loop
try:
    asyncio.get_event_loop().run_until_complete(
        start_server(find_gradient, download_zip)
    )
except KeyboardInterrupt:
    print(" Miner shutdown process complete.")

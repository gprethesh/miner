import json
import asyncio
import config  # Make sure config.py is in the same directory or properly referenced


async def request_job_file(websocket, message_type):
    try:
        # Create a message for requesting a file
        message = {
            "type": message_type,
            "wallet_address": config.WALLET_ADDRESS,
        }

        # Send the request message
        await websocket.send(json.dumps(message))

        # Wait for a response
        response = await websocket.recv()
        return response

    except Exception as e:
        print(f"An error occurred: {e}")

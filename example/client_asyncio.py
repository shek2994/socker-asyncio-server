import asyncio
import json
import re

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def send_message(self, message):
        reader, writer = await asyncio.open_connection(self.host, self.port)

        # Convert the Python dictionary to JSON string
        json_data = json.dumps(message)
        writer.write(json_data.encode('utf-8'))
        await writer.drain()

        data = await reader.read(1024)
        response = data.decode('utf-8')
        print(f"Received response from server: {response}")

        writer.close()
        await writer.wait_closed()

    @staticmethod
    def string_to_json(json_like_string):
        # Custom function to add single quotes around keys
        def add_single_quotes(match):
            return f'"{match.group(1)}":'

        # Add single quotes around keys
        modified_json_string = json_like_string
        modified_json_string = re.sub(r'([^,{\s]+):', add_single_quotes, modified_json_string)
        json_data = json.loads(modified_json_string)
        return json_data

if __name__ == "__main__":
    client = Client('127.0.0.1', 12345)

    # Example of using the string_to_json method
    json_like_string = '{step-1:{set-exp:50, set-dur:60, set-val:true},step-2:{set-exp:50, set-dur:60, set-val:true, set-type:{v:3, j:8}}}'
    json_data = client.string_to_json(json_like_string)
    print(json.dumps(json_data['step-1'], indent=4))

    asyncio.run(client.send_message(json_data['step-1']))

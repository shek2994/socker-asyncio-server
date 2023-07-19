# import asyncio
# import json

# class Server:
#     def __init__(self, host, port):
#         self.host = host
#         self.port = port

#     async def handle_request(self, reader, writer):
#         while True:
#             data = await reader.read(1024)
#             if not data:
#                 break

#             # Decode the received JSON string to Python dictionary
#             json_data = data.decode('utf-8')
#             message = json.loads(json_data)
#             print(f"Received message from client: {json.dumps(message, indent=4)}, {message.keys()}")

#             # Dummy logic to process the message
#             # Here, we just send a response back to the client
#             response = {"status": "success", "message": f"Received your message: {message}"}
#             json_response = json.dumps(response)
#             writer.write(json_response.encode('utf-8'))
#             await writer.drain()

#         writer.close()

#     async def start(self):
#         server = await asyncio.start_server(self.handle_request, self.host, self.port)

#         print(f"Server listening on {self.host}:{self.port}")

#         async with server:
#             await server.serve_forever()

# if __name__ == "__main__":
#     server = Server('127.0.0.1', 12345)
#     asyncio.run(server.start())

import asyncio
import json
import concurrent.futures

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def process_command(self, command, params):
        # Dummy logic to process the command with parameters
        # In this example, we just print the command and its parameters
        print(f"Received command: {command}, Parameters: {params}")

        # Add your actual logic to handle the command with parameters here


        result = "Command processed successfully"
        return result

    async def handle_request(self, reader, writer):
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break

                # Decode the received JSON string to Python dictionary
                json_data = data.decode('utf-8')
                message = json.loads(json_data)
                print(json.dumps(message))

                # Process each step in the message
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    for command, params in message.items():
                        print(command,params)

                        # Submit the command processing task to the thread pool
                        future = executor.submit(self.process_command, command, params)
                        # Wait for the task to complete (you can also set a timeout if needed)
                        future.result()

                print(future.result())
                # Dummy logic to send a response back to the client
                response = {"status": "success", "message": "Commands executed successfully"}
                json_response = json.dumps(response)
                writer.write(json_response.encode('utf-8'))
                await writer.drain()

        except Exception as e:
            print(f"Error occurred while processing client request: {e}")

        finally:
            writer.close()

    async def start(self):
        server = await asyncio.start_server(self.handle_request, self.host, self.port)

        print(f"Server listening on {self.host}:{self.port}")

        async with server:
            await server.serve_forever()

if __name__ == "__main__":
    server = Server('127.0.0.1', 12345)
    asyncio.run(server.start())

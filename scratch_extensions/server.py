# 导入websockets模块
import asyncio
import websockets
import socket

#def talkToDog():
#    global client_socket,dog_server_host,dog_server_port
#    client_socket.connect((dog_server_host, dog_server_port))
#    client_socket.sendall('i am client'.encode("utf-8"))
#    client_socket.close()

async def talkToDog(cmd):
    try:
        reader, writer = await asyncio.open_connection('localhost', 4000)
        writer.write(cmd.encode("utf-8"))
        await writer.drain()
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"An error occurred in talkToDog: {e}")

# 创建处理连接的方法
async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send("Received your message: " + message)
        await talkToDog(message)

# 创建WebSocket服务器
start_server = websockets.serve(echo, 'localhost', 3000)

# 与ee dog通信：socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# eedog服务器的主机和端口
dog_server_host = 'localhost'
dog_server_port = 4000

# 运行服务器
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

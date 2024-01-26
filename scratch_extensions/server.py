# 导入websockets模块
import asyncio
import websockets

# 创建处理连接的方法
async def echo(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        await websocket.send("Received your message: " + message)

# 创建WebSocket服务器
start_server = websockets.serve(echo, 'localhost', 3000)

# 运行服务器
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

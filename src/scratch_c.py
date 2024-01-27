import socket
import common

LOCAL_DEBUG = 1
if LOCAL_DEBUG == 1:
    ipAddr = 'localhost'
else:
    ipAddr = 0

addr = (ipAddr, 4000)                # 定义socket绑定的地址，ip地址为0，端口为90
mySocket = socket.socket()         # 创建一个socket对象
mySocket.bind(addr)                # 绑定地址
mySocket.listen(1)                 # 设置允许连接的客户端数量


while common.run_mode == common.MODE_scratch:
    client, addr = mySocket.accept()
    ret = client.recv(1024).decode("utf-8")
    print(ret)

    cmd, args = common.parseCMD(ret)
    common.execCMD(cmd, args)

mySocket.close()

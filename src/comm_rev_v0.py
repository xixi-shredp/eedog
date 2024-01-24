from machine import UART

uart = UART(2, baudrate=9600)


def ESPreceive():
    # data[0]表示命令种类 p:退出进程 m:移动 h:高度 g:姿态
    # data[1]至data[4]表示参数
    global uart
    data = uart.read(5)  # 从端口读5个字节
    if data == None:
        return None, None
    elif data[0] == ord('w'):
        return 'w', []
    elif data[0] == ord('m'):
        state = int.from_bytes(data[1:2], 'big', signed=True)
        speed = int.from_bytes(data[2:3], 'big', signed=True)
        return 'm', [state, speed]
    elif data[0] == ord('h'):
        height = int.from_bytes(data[1:2], 'big', signed=True)
        return 'h', [height]
    elif data[0] == ord('g'):
        PIT = int.from_bytes(data[1:2], 'big', signed=True)
        POL = int.from_bytes(data[2:3], 'big', signed=True)
        X = int.from_bytes(data[3:4], 'big', signed=True)
        return 'g', [PIT, POL, X]
    elif data[0] == ord('a'):
        mode = int.from_bytes(data[1:2], 'big', signed=True)
        return 'a', [mode]
    else:
        return None, None

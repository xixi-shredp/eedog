from machine import UART

uart = UART(2, baudrate=9600)


def ESPreceive():
    # data[0]表示命令种类 p:退出进程 m:移动 h:高度 g:姿态
    # data[1]至data[4]表示参数
    global uart
    data = uart.readline()
    if data != None:
        data = data.decode("utf-8")  # 从端口读5个字节
        data = data.split(',')
        data = [data[0]] + [int(i) for i in data[1:]]
    if data == None:
        return None, None
    elif data[0] == 'w':
        return 'w', []
    elif data[0] == 'm':
        state = data[1]
        speed = data[2]
        return 'm', [state, speed]
    elif data[0] == 'h':
        height = data[1]
        return 'h', [height]
    elif data[0] == 'g':
        PIT = data[1]
        POL = data[2]
        X = data[3]
        return 'g', [PIT, POL, X]
    elif data[0] == 'a':
        mode = data[1]
        return 'a', [mode]
    else:
        return None, None

from machine import UART

uart = UART(2, baudrate=9600)


def ESPreceive():
    # string[0]表示命令种类 p:退出进程 m:移动 h:高度 g:姿态
    # string[1]至string[4]表示参数

    global uart
    data = uart.read(5)  # 从端口读5个字节
    if data == None:
        return None, None
    if data[0] == ord('w'):
        return 'w', []
    elif data[0] == ord('m'):
        return 'm', [data[1], data[2]]
    elif data[0] == ord('h'):
        return 'h', [data[1]]
    elif data[0] == ord('g'):
        return 'g', [data[1], data[2], data[3]]
    elif data[0] == ord('a'):
        return 'a', [data[1]]
    else:
        return None, None

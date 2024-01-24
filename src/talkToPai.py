import padog
import comm_rev

s_idle, s_left, s_right, s_forward, s_backward = range(5)
m_talk, m_web = range(2)

mode = m_talk


def limit(_value, _max, _min):
    if (_value > _max):
        return _max
    elif (_value < _min):
        return _min
    else:
        return _value


def move(state, speed):
    global s_idle, s_left, s_right, s_forward, s_backward

    if state == s_idle:
        speed, L, R = 0, 0, 0
    elif state == s_left:
        speed, L, R = 1, 1, -1
    elif state == s_right:
        speed, L, R = 1, -1, 1
    elif state == s_forward:
        speed, L, R = speed, 1, 1
    elif state == s_backward:
        speed, L, R = -speed, 1, 1
    else:
        speed, L, R = 0, 0, 0
        print("state:", state, "is not support (0-4)")
    speed = limit(speed, -3, 6)  # -3 -> 6
    padog.move(speed, L, R)


# PIT俯仰角  ROL滚转轴  X：X轴位置  R_H：高度
# PIT    : -10  ->  10    default:0    unit:dec
# ROL    : -10  ->  10    default:0    unit:dec
# X      : -10  ->  40    default:0    unit:mm
def gesture(PIT, ROL, X):
    PIT = limit(PIT, -10, 10)
    ROL = limit(ROL, -10, 10)
    X = limit(X, -10, 40)
    padog.gesture(PIT, ROL, X)


# height :  70  -> 120    default:110  unit:mm
def height(h):
    h = limit(h, 70, 120)
    padog.height(h)


# 步态模式 ：0 -> walk   ;  1 -> tort
def gait(mode):
    if (mode != 0 and mode != 1):
        print("unsupported gait mode:   0:trot; 1:walk;")
    else:
        padog.gait(mode)


def change_to_web_mode():
    global mode, m_web
    mode = m_web


# 串口检测主控输入:5bytes   解码:命令+参数


def getDataFromPai():
    ret = comm_rev.ESPreceive()
    print(ret)
    return ret
    return 'm', [s_forward, 6]


# [cmd, description, handle_func, num_of_args]
cmd_table = [
    ['m', "move", move, 2],
    ['g', "gesture", gesture, 3],
    ['h', "height", height, 1],
    ['a', "gait", gait, 1],
    ['w', "web_c mode", change_to_web_mode, 0]
]

while mode == m_talk:
    cmd, args = getDataFromPai()  # 解码:命令+参数
    if cmd == None:
        continue
    # 解析命令行参数 ->  执行函数
    for cmd_info in cmd_table:
        cmd_to_compare = cmd_info[0]
        cmd_handle = cmd_info[2]
        num_of_args = cmd_info[3]

        if cmd == cmd_to_compare:
            if num_of_args == 0:
                cmd_handle()
            else:
                cmd_handle(*args[0:num_of_args])
            break


if mode == m_web:
    print("go to web_c")
else:
    print("error[talkToPai.py]:mode = ", mode,
          " is not supported, please reset again")

PC_DEBUG = 1
if PC_DEBUG == 0:
    import padog


# ----------------------------- run mode -------------------------------------
ModeList = (MODE_web_c, MODE_unknow1, MODE_unknow2, MODE_unknow3,
            MODE_talkToPai, MODE_scratch) = range(6)
run_mode = MODE_scratch

run_mode_help_info = """
 run_mode=0：web遥控模式
 run_mode=1：OpenMV 巡线模式
 run_mode=2：OpenMV 颜色识别模式
 run_mode=3：调试模式
 run_mode=4：串口通信模式
 run_mode=5：scratch 编程模式
"""


# ----------------------------- utils func ----------------------------------------

ANSI_FG_BLACK = "\33[1;30m"
ANSI_FG_RED = "\33[1;31m"
ANSI_FG_GREEN = "\33[1;32m"
ANSI_FG_YELLOW = "\33[1;33m"
ANSI_FG_BLUE = "\33[1;34m"
ANSI_FG_MAGENTA = "\33[1;35m"
ANSI_FG_CYAN = "\33[1;36m"
ANSI_FG_WHITE = "\33[1;37m"
ANSI_BG_BLACK = "\33[1;40m"
ANSI_BG_RED = "\33[1;41m"
ANSI_BG_GREEN = "\33[1;42m"
ANSI_BG_YELLOW = "\33[1;43m"
ANSI_BG_BLUE = "\33[1;44m"
ANSI_BG_MAGENTA = "\33[1;35m"
ANSI_BG_CYAN = "\33[1;46m"
ANSI_BG_WHITE = "\33[1;47m"
ANSI_NONE = "\33[0m"


def ANSI_FMT(meg: str, color: str):
    return color + meg + ANSI_NONE


def print_error(meg: str, *args):
    print(ANSI_FMT(meg, ANSI_FG_RED), args)


def limit(_value, _max, _min):
    if (_value > _max):
        return _max
    elif (_value < _min):
        return _min
    else:
        return _value


# ----------------------------- com func -----------------------------------------
s_idle, s_left, s_right, s_forward, s_backward = range(5)


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
    speed = limit(speed, 6, -3)  # -3 -> 6
    if PC_DEBUG == 0:
        padog.move(speed, L, R)
    else:
        print("dog move ", speed, L, R)


# PIT俯仰角  ROL滚转轴  X：X轴位置  R_H：高度
# PIT    : -10  ->  10    default:0    unit:dec
# ROL    : -10  ->  10    default:0    unit:dec
# X      : -10  ->  40    default:0    unit:mm
def gesture(PIT, ROL, X):
    PIT = limit(PIT, -10, 10)
    ROL = limit(ROL, -10, 10)
    X = limit(X, -10, 40)
    if PC_DEBUG == 0:
        padog.gesture(PIT, ROL, X)
    else:
        print("dog gesture", PIT, ROL, X)


# height :  70  -> 120    default:110  unit:mm
def height(h):
    h = limit(h, 70, 120)
    if PC_DEBUG == 0:
        padog.height(h)
    else:
        print("dog height ", h)


# 步态模式 ：0 -> walk   ;  1 -> tort
def gait(mode):
    if (mode != 0 and mode != 1):
        print("unsupported gait mode:   0:trot; 1:walk;")
    else:
        if PC_DEBUG == 0:
            padog.gait(mode)
        else:
            print("daog gait ", mode)


def change_run_mode(mode: int):
    global run_mode
    if mode not in ModeList:
        print_error("error:No such run mode", mode)
    else:
        run_mode = mode


def change_to_web_mode():
    change_run_mode(MODE_web_c)


def change_to_scratch_mode():
    change_run_mode(MODE_scratch)


# ----------------------------------- cmd --------------------------------------
# [cmd, description, handle_func, num_of_args]
cmd_table = [
    ['m', "move", move, 2],
    ['g', "gesture", gesture, 3],
    ['h', "height", height, 1],
    ['a', "gait", gait, 1],
    ['c', "change_run_mode", change_run_mode, 1],
    ['w', "change_to_web_c mode", change_to_web_mode, 0]
]

# example: "m,1,1"


def parseCMD(rec: str):
    if rec == "":
        print_error("empty cmd to parse")
        return "", []
    else:
        tem = rec.split(',')
        if len(tem) < 1:
            print_error("invalid cmd to parse", rec)
            return "", []
        elif len(tem) == 1:
            cmd = tem[0]
            args = []
        else:
            cmd = tem[0]
            args = [int(i) for i in tem[1:]]
        return cmd, args


def execCMD(cmd: str, args: list):
    if cmd == "":
        print_error("empty cmd to exec")
        return
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

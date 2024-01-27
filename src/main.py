import _thread
import padog
import time
from machine import Timer
from machine import UART
from padog import g, m
from machine import time_pulse_us
from machine import Pin
import common

common.run_mode = common.MODE_web_c

uart6 = UART(2, 115200)
t = Timer(1)

def OpenMV_Run(t):
    command = ""
    if uart6.any():
        read = uart6.read(1).decode('gbk')
        while read != '/':
            command = command + read
            read = uart6.read(1).decode('gbk')
        if (command != "1/") and command != "":
            try:
                exec(command)
                print("exec:", command)
            except:
                print("execerr:", command)
        command = ""
def app_1():
    exec(open('web_c.py').read())
def app_2():
    try:
        exec(open('my_code.py').read())
    except:
        print('积木编程代码执行出错，跳过...')
def serial_run_loop():
    while True:
        padog.mainloop()
def loop(t):
    padog.mainloop()


run_mode = common.run_mode
# 模式判定
if run_mode == common.MODE_web_c:
    # _thread.start_new_thread(app_1, ())
    t.init(period=10, mode=Timer.PERIODIC, callback=loop)
    exec(open("web_c.py").read())
elif run_mode == common.MODE_unknow1:
    t.init(period=50, mode=Timer.PERIODIC, callback=OpenMV_Run)
    padog.gesture(padog.in_pit, padog.in_rol, padog.in_y)
    padog.speed = 0.045
    serial_run_loop()
elif run_mode == common.MODE_unknow2:
    t.init(period=10, mode=Timer.PERIODIC, callback=OpenMV_Run)
    padog.gesture(padog.in_pit, padog.in_rol, padog.in_y)
    padog.speed = 0.045
    serial_run_loop()
elif run_mode == common.MODE_unknow3:
    _thread.start_new_thread(app_1, ())
    serial_run_loop()
elif run_mode == common.MODE_talkToPai:
    t.init(period=10, mode=Timer.PERIODIC, callback=loop)
    exec(open("talkToPai.py").read())
elif run_mode == common.MODE_scratch:
    t.init(period=10, mode=Timer.PERIODIC, callback=loop)
    exec(open("scratch_c.py").read())
else:
    print("not supported run mode: ", run_mode)
    print(common.run_mode_help_info)

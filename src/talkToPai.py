import padog
import common
import comm_rev


def getDataFromPai():
    ret = comm_rev.ESPreceive()
    print(ret)
    return ret


cmd_table = common.cmd_table

if __name__ == "__main__":
    while common.run_mode == common.MODE_talkToPai:
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

    if common.run_mode == common.MODE_web_c:
        print("go to web_c")
    else:
        common.print_error("error[talkToPai.py]", ":mode = ", common.run_mode,
                           " is not supported, please reset again")
        print(common.run_mode_help_info)

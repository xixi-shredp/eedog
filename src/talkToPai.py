import padog
import common
import comm_rev


# def getDataFromPai():
#     ret = comm_rev.ESPreceive()
#     print(ret)
#     return ret


cmd_table = common.cmd_table

if __name__ == "__main__":
    while common.run_mode == common.MODE_talkToPai:
        ret = comm_rev.ESPreceive()
        print(ret)
        cmd,args = common.parseCMD(ret)
        common.execCMD(cmd,args)

    if common.run_mode == common.MODE_web_c:
        print("go to web_c")
    else:
        common.print_error("error[talkToPai.py]", ":mode = ", common.run_mode,
                           " is not supported, please reset again")
        print(common.run_mode_help_info)

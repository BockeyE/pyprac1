import os
import threading


def opencmd(strs):
    cmd = "dir"
    os.system(cmd)
    print(strs)
    global t
    t = threading.Timer(60*30, opencmd, ["aaa"])
    t.start()


if __name__ == '__main__':
    t = threading.Timer(2, opencmd, ["aaa"])
    t.start()

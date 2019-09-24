import psutil
import time
from tkinter import *


def make_app():
    app = Tk()
    app.geometry('200x100')
    app.config(bg='#303030')
    Label(text='实时网速监控', font=('Hack', 23, 'bold'), bg='#303030', fg='white').pack()
    Label(name='lb2', text='_kb/s', font=('Hack', 20, 'bold'), bg='#303030', fg='white').pack()
    return app


def speed_test():
    s1 = psutil.net_io_counters(pernic=True)['以太网']
    time.sleep(1)
    s2 = psutil.net_io_counters(pernic=True)['以太网']
    result = s2.bytes_recv - s1.bytes_recv
    # 除法结果保留两位小数
    return str('%.2f' % (result / 1024)) + 'kb/s'


def ui_updata(do):
    data = do()
    # app下名字是lb2的子控件
    lb2 = app.children['lb2']
    # 配置，替换原来的text
    lb2.config(text=data)
    # 每1秒后调用lambda:ui_updata(do)函数
    app.after(1000, lambda: ui_updata(do))


app = make_app()
# 每1秒后调用ui_updata(speed_test)函数
app.after(1000, lambda: ui_updata(speed_test))
app.mainloop()

import time

from pynput.keyboard import Key, Controller as KC, Listener

keyboard = KC()
## 监听键盘

from pynput.mouse import Button, Controller as MC

mouse = MC()


# r回溯3s延迟，记录鼠标坐标
# q，0.8s，弹道时间预计0.3s
# w,1.5s


def on_press(key):
    if type(key) == Key:
        pass
    else:
        if key.char == 'y':
            pos = mouse._position_get()
            print('enter y')
            while True:
                mouse.position = (pos[0], pos[1])
                mouse.press(Button.left)
                mouse.release(Button.left)
                print('presys done')
                time.sleep(5)


def on_release(key):
    pass


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

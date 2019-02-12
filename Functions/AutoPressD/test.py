import time

from pynput.keyboard import Key, Controller

keyboard = Controller()
# # 按键盘和释放键盘
# keyboard.press(Key.space)
# keyboard.release(Key.space)
#
# # 按小写的a
# keyboard.press('a')
# keyboard.release('a')
#
# # 按大写的A
# keyboard.press('A')
# keyboard.release('A')

# # 按住shift在按a
# with keyboard.pressed(Key.shift):
#     # Key.shift_l, Key.shift_r, Key.shift
#     keyboard.press('a')
#     keyboard.release('a')

# # 直接输入Hello World
# keyboard.type('Hello World')

## 监听键盘
from pynput.keyboard import Key, Listener


def on_press(key):
    # 监听按键
    print('{0} pressed'.format(key))
    if type(key) == Key:
        pass
    else:
        if key.char == 'd':
            time.sleep(0.5)
            keyboard.press('d')
            print('d 0.1s later')
            return


def on_release(key):
    # 监听释放
    print('{0} release'.format(key))
    print(key)
    # if key == Key.esc:
    #     # Stop listener
    #     return False

    # Stop listener


# 连接事件以及释放
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

import random
import time
from pynput.keyboard import Key, Listener, Controller

keyboard = Controller()


def on_press(key):
    if type(key) == Key:
        return
        # else:
    #     if key.char == '9':
    #         flag = flag + 1
    #         return
    #     elif key.char == '8':
    #         flag = flag - 3
    #         return
    #     elif flag == 3 and key.char == 'd':
    if key.char == 'd':
        r = random.randint(42, 58)
        keyboard.press('g')
        keyboard.release('g')
        time.sleep(r / 100)
        keyboard.press('g')
        keyboard.release('g')
        time.sleep(2)
        keyboard.press('g')
        keyboard.release('g')
        print('2  attack combs  after  ' + str(r / 100))
        return


def on_release(key):
    pass


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

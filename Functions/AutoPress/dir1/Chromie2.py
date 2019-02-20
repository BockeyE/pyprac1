import time
from pynput.mouse import Button, Controller as MC
from pynput.keyboard import Key, Controller as KC, Listener

keyboard = KC()
mouse = MC()


def on_press(key):
    if type(key) == Key:
        pass
    else:
        if key.char == 'y':
            pos = mouse._position_get()
            print(pos)
            keyboard.press('r')
            keyboard.release('r')
            time.sleep(1.6)
            mouse.position = (pos[0], pos[1])
            keyboard.press('w')
            keyboard.release('w')
            time.sleep(0.5)
            mouse.position = (pos[0], pos[1])
            keyboard.press('q')
            keyboard.release('q')
            print('combo done')
            return


def on_release(key):
    pass


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

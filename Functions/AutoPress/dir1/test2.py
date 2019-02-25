from pynput.mouse import Button, Controller as MC

mouse = MC()

pos = mouse._position_get()
print(pos)
mouse.position=(400, 400)
pos = mouse._position_get()
print(pos)
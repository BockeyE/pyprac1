import os

from click._compat import raw_input

cmd = "sc config i8042prt start= auto"
os.system(cmd)
print('======end=======')
c = raw_input()

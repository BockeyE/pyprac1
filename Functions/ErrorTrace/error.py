import traceback

try:
    s = 1 / 0;
except Exception as e:
    exstr = traceback.format_exc()
    traceback.print_exc()
    print(exstr)

print(2)

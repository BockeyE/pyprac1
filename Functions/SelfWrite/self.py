path = os.path.join(os.path.dirname(__file__), "../contract/contract_header.py")
with open(path, 'r') as f:
    contract_header = f.read()
path = os.path.join(os.path.dirname(__file__), "../contract/contract_footer.py")
with open(path, 'r') as f:
    contract_footer = f.read()


rr = re.search("class \s*(\w*)\W*Contract\s*", ass["data"])
if rr:
    path = os.path.join("/root", id + ".py")
    f = open(path, 'w')  # 若是'wb'就表示写二进制文件
    f.write(contract)
    f.close()
    process = os.popen("python3 " + path)  # return file
    output = process.read()
    process.close()
    print(output)

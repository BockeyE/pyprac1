path = os.path.join(os.path.dirname(__file__), "../contract/contract_header.py")
with open(path, 'r') as f:
    contract_header = f.read()
path = os.path.join(os.path.dirname(__file__), "../contract/contract_footer.py")
with open(path, 'r') as f:
    contract_footer = f.read()
contract = deepcopy(contract_header)
transaction = BigchainDB().get_assets(tx_id)
contract = contract.replace("TURING_CONTRACT_TXID", tx_id)
contract = contract.replace("TURING_CONTRACT_OWNER_BEFORE", transaction.inputs[0].owners_before[0])

if "data" in transaction.asset and "code" in transaction.asset["data"] and "call" in transaction.metadata:
    contract = contract + transaction.asset["data"]["code"] + deepcopy(contract_footer)
    rr = re.search("class \s*(\w*)\W*Contract\s*", transaction.asset["data"]["code"])
    if rr:
        classname = rr.group(1)
        contract = contract.replace("CONTRACT_CLASS_NAME", classname)
        contract = contract.replace("CONTRACT_FUNCTION", call)
        path = os.path.join("/root", transaction.id + ".py")
        f = open(path, 'w')  # 若是'wb'就表示写二进制文件
        f.write(contract)
        f.close()
        process = os.popen("python3 " + path)  # return file
        output = process.read()
        process.close()
        print(output)
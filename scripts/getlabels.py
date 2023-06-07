import json
from os import listdir, path, walk


def main():
    sanc_directory = '../smart-contract-sanctuary-ethereum/contracts/mainnet'
    label_directories = [
        '../etherscan-labels-main/data/etherscan/accounts',
        '../etherscan-labels-main/data/etherscan/tokens'
    ]

    labels = ['advertising','auction','bridge','charity','closure','donate','defi',
    'dex','e-commerce','farming','fiat-gateway','fund','layer-2','ico-walltes',
    'investment','liquidity','mining','news','payment','router','staking']

    contracts = {}
    for directory in label_directories:
        for filename in listdir(directory):
            fileparts = filename.split(".")
            if fileparts[0] in labels and fileparts[1] == "json":
                file_path = path.join(directory, filename)
                with open(file_path) as json_file:
                    label = path.splitext(filename)[0]
                    data = json.load(json_file)
                    for contract_addr, name in data.items():
                        # print(contract_addr)
                        if contract_addr.lower() in contracts: 
                            contracts[contract_addr.lower()]["labels"] += [label]
                        else:
                            contracts[contract_addr.lower()] = {"labels": [label]}
    print("found contracts in etherscan-labels-main: " + str(len(contracts)))

    total_count = 0
    labelled_contracts = {}
    for root, directories, files in walk(sanc_directory):
        for filename in files:
            total_count += 1
            contract_addr = "0x" + filename.split("_")[0].lower()
            # print(contract_addr)
            if contract_addr in contracts:
                labelled_contracts[contract_addr] = contracts[contract_addr]
    print("found contracts in smart-contract-sanctuary-ethereum: " + str(total_count))
    print("mapped contracts: " + str(len(labelled_contracts)))

    json_object = json.dumps(labelled_contracts)
    with open("labelled_contracts.json", "w") as outfile:
        outfile.write(json_object)


if __name__ == "__main__":
    main()

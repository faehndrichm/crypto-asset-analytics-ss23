import os
import os.path as path

import pandas as pd

addresses = []

sanc_dir = path.join('..', '..', 'smart-contract-sanctuary', 'ethereum', 'contracts', 'mainnet')
total_count = 0
for root, directories, files in os.walk(sanc_dir):
    for filename in files:
        total_count += 1
        contract_addr = "0x" + filename.split("_")[0].lower()
        print(contract_addr)
        addresses.append(contract_addr)

df = pd.DataFrame(addresses)
df.to_csv("sanc_eth_mainnet.csv", index=None)
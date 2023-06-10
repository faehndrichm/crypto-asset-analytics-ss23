import requests
import argparse
import time
import os, os.path as path
import sys
import yaml
import json

with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

def getABI(ca_addr,apiKey=config["keys"]["etherscan"]):
    print(f"getting ABI for {ca_addr}")
    base_url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={ca_addr}&apiKey={apiKey}"
    r = requests.get(base_url)
    d = r.json()['result']
    return d

def saveABI(ca_addr, base_dir):
    filename = f"{ca_addr}.abi.json"
    if not path.exists(filename):
        abi = getABI(ca_addr) 
        with open(path.join(base_dir, filename), 'wb') as fj:
            fj.write(abi.encode('utf8')) 

def main(args):
    if args.fromfile and path.exists(args.fromfile):
        with open(args.fromfile) as fl:
            skipped = 0
            for line in fl:
                #print(line)
                if args.skip is not None and skipped < args.skip:
                    skipped += 1
                    continue
                 
                if args.separator in line:
                    parts = line.split(args.separator)
                    addr = parts[args.colidx]
                    saveABI(addr.strip(), args.outdir)

                if args.skip is not None and args.skip > 1:
                    msskip = 1000 // (args.skip-1)
                    time.sleep(msskip)

    elif args.address is not None:
        saveABI(args.address, args.outdir)        


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-address', required=False)
    parser.add_argument('-fromfile', help='read list of addresses from text file', required=False)
    parser.add_argument('-separator', default=',', help='separator symbol', required=False)
    parser.add_argument('-colidx', type=int, default=0, help='', required=False)
    parser.add_argument('-outdir', help='output directory', required=False)
    parser.add_argument('-limit', type=int, help='max request per second')
    parser.add_argument('-skip', type=int, help="skip n first lines")

    args = parser.parse_args()
    
    if args.outdir is None:
        args.outdir = os.getcwd()

    main(args)
import requests
import argparse
import time
import os, os.path as path
import sys
import yaml
import json
import shutil

with open('config.yml') as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

NUM_REQ = 0

def check_repo(ca_addr, repo_dir, base_dir):
    tdir = ca_addr[2:4]
    rpath = path.join(repo_dir, tdir, f"{ca_addr}.abi.json")
    bpath = path.join(base_dir, tdir, f"{ca_addr}.abi.json")
    if path.exists(rpath) and not path.exists(bpath):
        if not path.exists(path.join(base_dir, tdir)):
            os.makedirs(path.join(base_dir, tdir))
        print(f"getting ABI for {ca_addr} from cache")
        shutil.copy2(rpath, bpath)
        return True
    return False

def getABI(ca_addr,apiKey=config["keys"]["etherscan"]):
    global NUM_REQ
    print(f"getting ABI for {ca_addr}")
    base_url = f"https://api.etherscan.io/api?module=contract&action=getabi&address={ca_addr}&apiKey={apiKey}"
    r = requests.get(base_url)
    NUM_REQ += 1
    d = r.json()['result']
    return d

def saveABI(ca_addr, base_dir):
    tdir = ca_addr[2:4]
    if not path.exists(path.join(base_dir, tdir)):
        os.makedirs(path.join(base_dir, tdir))
    filename = path.join(base_dir, tdir, f"{ca_addr}.abi.json")
    if not path.exists(filename):
        abi = getABI(ca_addr) 
        with open(filename, 'wb') as fj:
            fj.write(abi.encode('utf8')) 

def main(args):
    nline = 0
    uniqueaddr = []
    if args.fromfile and path.exists(args.fromfile):
        with open(args.fromfile) as fl:
            skipped = 0
            for line in fl:
                # print(line)
                
                nline += 1
                if args.skip is not None and skipped < args.skip:
                    print("skip")
                    skipped += 1
                    continue

                if NUM_REQ > args.maxreq:
                    print("limit reached")
                    break

                addr = line 
                if args.separator in addr:
                    parts = addr.split(args.separator)
                    addr = parts[args.colidx]
                
                uniqueaddr += [addr]
                tdir = addr[2:4]
                rpath = path.join(args.repodir, tdir, f"{addr}.abi.json")
                bpath = path.join(args.outdir, tdir, f"{addr}.abi.json")
                if(path.exists(bpath)):
                    nline += 1

                if args.repodir is None or not check_repo(addr.strip(), args.repodir, args.outdir):
                    saveABI(addr.strip(), args.outdir)

                if args.skip is not None and args.skip > 1:
                    msskip = 1000 // (args.skip-1)
                    time.sleep(msskip)
        print(f"{nline} {NUM_REQ} {len(uniqueaddr)} {len(list(set(uniqueaddr)))}")
    elif args.address is not None:
        saveABI(args.address, args.outdir)        


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-address', required=False)
    parser.add_argument('-fromfile', help='read list of addresses from text file', required=False)
    parser.add_argument('-separator', default=',', help='separator symbol', required=False)
    parser.add_argument('-colidx', type=int, default=0, help='', required=False)
    parser.add_argument('-outdir', help='output directory', required=False)
    parser.add_argument('-repodir', help='directory containing downloaded ABI for lookup')
    parser.add_argument('-limit', type=int, default=5, help='max request per second')
    parser.add_argument('-skip', type=int, help="skip n first lines")
    parser.add_argument('-maxreq', type=int, default=50000, help="limit total number of request")

    args = parser.parse_args()
    
    if args.outdir is None:
        args.outdir = os.getcwd()

    if not path.exists(args.outdir):
        os.makedirs(args.outdir)

    if args.fromfile is not None and not path.exists(args.fromfile):
        print("file not found")
        sys.exit(1)

    main(args)
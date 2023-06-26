import os
import os.path as path
import argparse

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir')
    args = parser.parse_args()

    sanc_dir = path.join(args.inputdir)
    total_count = 0
    total_unverified = 0
    for root, directories, files in os.walk(sanc_dir):
        # print(root, directories, files)
        stop = False
        for filename in files:
            total_count += 1
            fullfile = path.join(root, filename)
            if path.exists(fullfile):
                base, ext = path.splitext(fullfile)
                # print(filename, ext)
                if ext == '.kg':
                    print(filename)
                    os.system(f"type {fullfile} >> scs_eth_mainnet.tsv")
        #             stop = True
        #             break
        # if stop: break
    #         with open(fullfile) as fi:
    #             content = fi.read()
    #         if not content.startswith('['):
    #             # the document is not a JSON document (text "The Contracts is not verified")
    #             print(fullfile)
    #             total_unverified += 1
    # print(f"{total_unverified} / {total_count} : {total_count-total_unverified}")        
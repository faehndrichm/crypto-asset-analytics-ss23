import os
import os.path as path
import argparse
from abi2kg import abi2kg

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('inputdir')
    parser.add_argument('-outputdir')
    args = parser.parse_args()

    sanc_dir = path.join(args.inputdir)
    total_count = 0
    total_unverified = 0
    stop = False
    for root, directories, files in os.walk(sanc_dir):
        # print(root, directories, files)
        for filename in files:
            total_count += 1
            fullfile = path.join(root, filename)
            
            if path.exists(fullfile):
                with open(fullfile) as fi:
                    content = fi.read()
                if content.startswith('['):
                    base, ext = path.splitext(filename)
                    basedir = path.basename(root)
                    outdir = path.join(args.outputdir, basedir)
                    if not path.exists(outdir):
                        os.makedirs(outdir)
                    newfile = path.join(outdir, f"{base}.kg")
                    if not path.exists(newfile):
                        try:
                            abi2kg(fullfile, newfile)
                        except:
                            print(content)                
                            stop = True
                            break
        if stop: break
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
        for filename in files:
            total_count += 1
            fullfile = path.join(root, filename)
            # print(fullfile)
            with open(fullfile) as fi:
                content = fi.read()
            if not content.startswith('['):
                # the document is not a JSON document (text "The Contracts is not verified")
                print(fullfile)
                total_unverified += 1
    print(f"{total_unverified} / {total_count} : {total_count-total_unverified}")        
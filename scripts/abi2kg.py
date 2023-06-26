import json
import argparse
import os
import os.path as path
import sys

def abi2kg(abifile, kgfile, format='tsv'):
    base, _ = path.splitext(abifile)
    base, _ = path.splitext(base)
    addr = path.basename(base)
    print(addr)
    with open(abifile) as fj:
        abijson = json.loads(fj.read())

    triples = []

    addr_node = addr
    triples.append((addr_node, 'type', 'SmartContractAddress'))
    for item in abijson:
        itype = item['type']
        if itype not in ['event', 'function']: continue
        iname = itype + '/' + item['name']
        if itype == 'event':
            # print(json.dumps(item,indent=2))
            triples.append((addr_node, 'has_event', iname))
        elif itype == 'function':
            triples.append((addr_node, 'has_function', iname))
        if 'inputs' in item and len(item['inputs'])>0:
            for arg in item['inputs']:
                arg_node = item['name'] + '/' + arg['name']
                triples.append((iname, 'has_input', arg_node))
                triples.append((arg_node, 'has_type', arg['type']))
        if 'outputs' in item and len(item['outputs'])>0:
            for arg in item['outputs']:
                arg_node = item['name'] + '/' + 'output'
                triples.append((iname, 'has_output', arg_node))
                triples.append((arg_node, 'has_type', arg['type']))

            
    if format == 'tsv':
        content = '\n'.join(['\t'.join(triple) for triple in triples]).lower()
        # print(content)
        with open(kgfile, 'w') as kg:
            kg.write(content)


def main(args):
    abi2kg(args.abifile, args.kgfile)
    

if __name__=="__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('abifile')
    parser.add_argument('-kgfile')
    parser.add_argument('-format', choices=['tsv', 'rdf'], default='tsv')

    args = parser.parse_args()

    if not path.exists(args.abifile):
        sys.exit(1)

    if args.kgfile is None:
        base, ext = path.splitext(args.abifile)
        if args.format == 'tsv':
            args.kgfile = base + '.' + args.format
        elif args.format == 'rdf':
            args.kgfile = base + '.nt'

    main(args)
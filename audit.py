import os
import hashlib
import argparse
import json
import logging

'''
Given the path to a directory, generate a manifest file
'''

dirs_to_audit = ['code', 'data', 'docs']


def get_md5(filepath):
    return hashlib.md5(open(filepath, 'rb').read()).hexdigest()


def make_website():
    '''
    import plotly and make something?
    '''
    pass


def main(root):
    '''
    Iterate through each file in the repository and check a hash
    '''
    answer = {
        'name': os.path.basename(root)
    }

    data = []
    for file in os.listdir(root):
        if os.path.isdir(file) and file in dirs_to_audit:
            filepath = os.path.join(os.path.join(root, dir), file)
            data.append(
                {
                    'name': file,
                    'md5': get_md5(filepath),
                    'size': os.path.getsize(path),
                }
            )
    answer['data'] = data
    logging.info('Manifest file: %s' % answer)
    export_file = 'manifest.json'
    with open(export_file, 'w') as f:
        json.dump(data, f)
    logging.info('[%s] Manifest file created' % os.path.isfile(export_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='UVA BI SDAD audit a Data Repository')
    parser.add_argument('-i', '--input_root', type=str,
                        help='The root directory that needs to be audited')
    parser.add_argument('-v', '--verbose',
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    if not os.path.isdir(args.input_root):
        print('%s is not a directory' % (args.input_root))
    else:
        main(args.input_root)

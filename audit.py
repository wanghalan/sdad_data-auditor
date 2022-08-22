import os
import hashlib
import argparse
import json
import logging
from pathlib import Path

'''
Given the path to a directory, generate a manifest file
[Finding files recursively] https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
'''


def get_md5(filepath):
    return hashlib.md5(open(filepath, 'rb').read()).hexdigest()


def make_website():
    '''
    import plotly and make something?
    '''
    pass


def evaluate_folder(data, dirpath, prepend='https://raw.githubusercontent.com/uva-bi-sdad/'):
    '''
    Given a directory, add all file information into data
    Assume if it is under a distribution folder, to store the manifest for this data
    '''
    logging.debug('Evaluating folder: %s' % dirpath)

    for path in Path(dirpath).rglob('distribution/**/*'):
        logging.debug('\tEvaluating: %s' % path.name)

        if os.path.isfile(path):
            data.append(
                {
                    'name': path.name,
                    # Append the raw github location, add the repository name after, and then add the path under the repository
                    'path': prepend + os.path.join(os.path.basename(os.path.abspath(args.input_root)), os.path.relpath(path)),
                    'md5': get_md5(path),
                    'size': os.path.getsize(path),
                }
            )


def main(root, prepend, test=False):
    '''
    Iterate through each file in the repository and check a hash
    '''
    root = os.path.abspath(root)
    answer = {
        'name': os.path.basename(root)
    }

    data = []
    for file in os.listdir(root):
        logging.debug(file)
        dirpath = os.path.join(root, file)
        if os.path.isdir(dirpath):
            logging.debug('%s is a related directory' % (dirpath))
            evaluate_folder(data, dirpath, prepend)

    answer['data'] = data
    answer['count'] = len(data)
    logging.info('Manifest file: %s' %
                 json.dumps(answer, indent=4, sort_keys=True))
    # export the file to root
    if not test:
        export_file = os.path.join(root, 'manifest.json')
        with open(export_file, 'w') as f:
            json.dump(answer, f)
        logging.info('[%s] Manifest file created' %
                     os.path.isfile(export_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='UVA BI SDAD audit a Data Repository')
    parser.add_argument('-i', '--input_root', type=str,
                        help='The root directory that needs to be audited', required=True)
    parser.add_argument('-v', '--verbose',
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('-t', '--test',
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('-p', '--prepend', type=str,
                        help='Raw github url to prepend')

    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    prepend = None
    if args.prepend:
        prepend = args.prepend
    else:
        prepend = 'https://raw.githubusercontent.com/uva-bi-sdad/'

    if not os.path.isdir(args.input_root):
        logging.info('%s is not a directory' % (args.input_root))
    else:
        logging.info('Auditing: %s' % os.path.abspath(args.input_root))
        main(args.input_root, prepend, args.test)

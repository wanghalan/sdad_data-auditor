import os
import hashlib
import argparse
import json
import logging

'''
Given the path to a directory, generate a manifest file
'''

dirs_to_audit = ['code', 'data', 'docs']
file_end_to_record=['xz']

def get_md5(filepath):
    return hashlib.md5(open(filepath, 'rb').read()).hexdigest()


def make_website():
    '''
    import plotly and make something?
    '''
    pass


def evaluate_folder(data, dirpath):
    '''
    Given a directory, add all file information into data
    '''
    logging.debug('Evaluating folder: %s' % dirpath)
    for child_file in os.listdir(dirpath):
        logging.debug('\tEvaluating: %s' % child_file)
        filepath = os.path.join(dirpath, child_file)
        if os.path.isdir(filepath):
            evaluate_folder(data, filepath)
        if os.path.isfile(filepath) and child_file.split('.')[-1] in file_end_to_record:
            data.append(
                {
                    'name': child_file,
                    'path': os.path.relpath(filepath),
                    'md5': get_md5(filepath),
                    'size': os.path.getsize(filepath),
                }
            )


def main(root, test=False):
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
        if os.path.isdir(dirpath) and file in dirs_to_audit:
            logging.debug('%s is a related directory' % (dirpath))
            evaluate_folder(data, dirpath)

    answer['data'] = data
    answer['count'] = len(data)
    logging.info('Manifest file: %s' %
                 json.dumps(answer, indent=4, sort_keys=True))
    # export the file to root
    if not test:
        export_file = os.path.join(root, 'manifest.json')
        with open(export_file, 'w') as f:
            json.dump(answer, f)
        logging.info('[%s] Manifest file created' % os.path.isfile(export_file))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='UVA BI SDAD audit a Data Repository')
    parser.add_argument('-i', '--input_root', type=str,
                        help='The root directory that needs to be audited', required=True)
    parser.add_argument('-v', '--verbose',
                        action=argparse.BooleanOptionalAction)
    parser.add_argument('-t', '--test',
                        action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(format='%(levelname)s: %(message)s', level=log_level)

    if not os.path.isdir(args.input_root):
        logging.info('%s is not a directory' % (args.input_root))
    else:
        logging.info('Auditing: %s' % os.path.abspath(args.input_root))
        main(args.input_root, args.test)

# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 04:21:26 2019

@author: GRENTOR
"""
import os
import argparse
import sys
import logging
#from tqdm import tqdm
from merge_files import Merge

def get_parser():
    """
    gets & parses arguments from command line
    """
    parser = argparse.ArgumentParser(
        description="Merges different JSON files into a single JSON object in a new file",
        add_help=True)
    parser.add_argument('-ip',
                        dest = "input_prefix",
                        help="Input prefix",
                        required=True)
    parser.add_argument('-op',
                        dest = "output_prefix",
                        help="Output prefix",
                        required=True)
    parser.add_argument('-maxFileSize',
                        dest = "max_file_size",
                        help="The maximum file size (in bytes) that each merged file should have",
                        type=int,
                        required=True
                        )
    parser.add_argument('-dir_path',
                        dest ="data_dir",
                        help="Path to directory where all json files are stored",
                        required=True)
    parser.add_argument('-log_level',
                        dest="log_level",
                        help="The logging level - defaults to INFO",
                        metavar = "{'INFO','DEBUG','ERROR'}",
                        choices = ['INFO', 'DEBUG', 'ERROR'],
                        default="INFO")
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)
    return parser.parse_args()


logger = logging.getLogger(__name__)
def configure_logger(log_level):
    """
    configures the logger object
    """

    if not logger.handlers:
        # Prevent logging from propagating to the root logger
        logger.propagate = 0
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
        logger.setLevel(logging.DEBUG)
        stream_handler.setLevel(log_level)
        stream_handler.setFormatter(log_formatter)
        logger.addHandler(stream_handler)
def output_folder(data_dir):
    """
    Creates new output folder for merged files to be stored in
    """
    i = 1
    path = os.path.join(data_dir, 'MergedFiles')
    while os.path.exists(path):
        path = os.path.join(data_dir, 'MergedFiles'+str(i))
        i += 1
    os.mkdir(path)
    return path

def path_creator(data_dir, prefix):
    """
    Creates a path with prefix at end
    """
    return os.path.join(data_dir, prefix)

class Error(Exception):
    """Base class for other exceptions"""

class FolderNotFoundError(Error):
    """Raised when the Folder path is not found"""

def main():
    """
    Driver Function
    """
    try:
        args = get_parser()
        configure_logger(args.log_level)
        if not os.path.exists(args.data_dir):
            raise FolderNotFoundError
        if not os.path.isfile('{}{}'.format
        (path_creator(args.data_dir, args.input_prefix), '1.json')):
            raise FileNotFoundError

        merge = Merge(path_creator(args.data_dir, args.input_prefix),
                      path_creator(args.data_dir, args.output_prefix),
                      args.max_file_size)

        merge.merge()

    except FileNotFoundError:
        logger.error('Please check the input prefix !!')
    except FolderNotFoundError:
        logger.error('No such directory exists !!')
    except ValueError:
        logger.error('File size larger than given Max File Size !!')


if __name__ == '__main__':
    main()

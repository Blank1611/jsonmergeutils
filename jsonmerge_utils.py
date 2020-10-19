# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 04:21:26 2019

@author: GRENTOR
"""
import os
import logging
#from tqdm import tqdm
from merge_files import Merge
logger = logging.getLogger(__name__)
def configure_logger():
    """
    configures the logger object
    """
    logging.basicConfig(filename='output.log', level=logging.INFO)
    if not logger.handlers:
        # Prevent logging from propagating to the root logger
        logger.propagate = 0
        log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        stream_handler = logging.StreamHandler()
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
        configure_logger()
        data_dir = input('Folder Path: ')
        if not os.path.exists(data_dir):
            raise FolderNotFoundError
        input_prefix = input('I/P Prefix: ')
        if not os.path.isfile('{}{}'.format(path_creator(data_dir, input_prefix), '1.json')):
            raise FileNotFoundError
        output_prefix = input('O/P Prefix: ')
        max_file_size = int(input('Max File Size: '))

        merge = Merge(path_creator(data_dir, input_prefix),
                      path_creator(data_dir, output_prefix),
                      max_file_size)

        merge.merge()

    except FileNotFoundError:
        logger.error('Please check the input prefix !!')
    except FolderNotFoundError:
        logger.error('No such directory exists !!')
    except ValueError:
        logger.error('File size larger than given Max File Size !!')


if __name__ == '__main__':
    main()

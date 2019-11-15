# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 04:21:26 2019

@author: GRENTOR
"""
import json
import os
#from tqdm import tqdm
from merge_files import merge_object
from merge_files import Merge


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

def file_list(data_dir, input_prefix):
    """
    Lists the json files with the given input prefix
    """
    i = 1
    path = os.path.join(data_dir, input_prefix+str(i)+'.json')
    while os.path.isfile(path):
        yield path
        i += 1
        path = os.path.join(data_dir, input_prefix+str(i)+'.json')

def main():
    """
    Driver Function
    """
    data_dir = input('Folder Path: ')
    input_prefix = input('I/P Prefix: ')
    output_prefix = input('O/P Prefix: ')
    max_file_size = int(input('Max File Size: '))
    end = False
    merger, root_keys = merge_object(os.path.join(data_dir, input_prefix+str(1)+'.json'))
    merge = Merge(data_dir, output_prefix, max_file_size, merger, root_keys)
    count = 0
    for i in file_list(data_dir, input_prefix):
        print(i)
        with open(i) as input_file:
            obj = json.load(input_file)
            merge.merge_file(obj, end)
        count+=1
    end = True
    merge.merge_file(None, end)
    print('{} Files Processed'.format(count))
    print('Done!!')

if __name__ == '__main__':
    main()

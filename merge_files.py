# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:34:18 2019

@author: GRENTOR
"""
import logging
import json
import os
from jsonmerge import Merger
from schema_modified import schema_builder

logger = logging.getLogger("jsonmerge-logger")

def merge_object(data_dir, max_file_size):
    """"
    Generates and returns a merge object for merging files
    """
    with open(data_dir) as input_file:
        obj = json.load(input_file)
        if sizeof(obj) > max_file_size:
            raise ValueError
        return Merger(schema_builder(obj)), list(obj.keys())

def sizeof(obj):
    """
    Returns size of json string
    """
    if obj:
        return len(json.dumps(obj))
    return 0

class Merge:
    """
    Merge class for merging json files
    """
    def __init__(self, input_path, output_path, max_file_size):
        self.base = None
        self.output_path = output_path
        self.input_path = input_path
        self.max_file_size = max_file_size
        self.counter = 1
        self.merger, self.root_keys = merge_object(
            '{}{}'.format(self.input_path, '1.json'),
            self.max_file_size)

    def redundant_obj(self):
        """
        Removes redundant data
        """
        for i in self.root_keys:
            set_of_jsons = {json.dumps(d, sort_keys=False) for d in self.base[i]}
            self.base[i] = [json.loads(t) for t in set_of_jsons]

    def file_list(self):
        """
        Lists the json files with the given input prefix
        """
        i = 1
        path = '{}{}{}'.format(self.input_path, i, '.json')
        while os.path.isfile(path):
            yield path
            i += 1
            path = '{}{}{}'.format(self.input_path, i, '.json')

    def merge(self):
        """
        merging driver function
        """
        end = False
        count = 0
        for i in self.file_list():
            logger.info(i)
            with open(i) as input_file:
                obj = json.load(input_file)
                self.merge_file(obj, end)
            count += 1
        end = True
        self.merge_file(None, end)
        logger.info('Done!!')
        logger.info('%d Files Processed', count)
        logger.info('%d Result files created', self.counter)

    def merge_file(self, head, end):
        """
        Merges the files and writes to json file upon reaching limit
        """
        base_size = sizeof(self.base)
        head_size = sizeof(head)
        if head_size > self.max_file_size:
            raise ValueError
        if not end:
            if (base_size < self.max_file_size) and ((base_size+head_size) <= self.max_file_size):
                self.base = (self.merger).merge(self.base, head)
                #self.redundant_obj()
            else:
                path = '{}{}{}'.format(self.output_path, self.counter, '.json')
                with open(path, 'w', encoding='utf-8') as output_file:
                    json.dump(self.base, output_file, ensure_ascii=False)
                self.counter += 1
                self.base = None
                self.base = (self.merger).merge(self.base, head)
        else:
            if self.base:
                path = '{}{}{}'.format(self.output_path, self.counter, '.json')
                with open(path, 'w', encoding='utf-8') as output_file:
                    json.dump(self.base, output_file, ensure_ascii=False)

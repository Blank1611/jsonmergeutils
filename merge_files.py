# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:34:18 2019

@author: GRENTOR
"""
import json
import os
from jsonmerge import Merger
from schema_modified import schema_builder

def merge_object(data_dir):
    """"
    Generates and returns a merge object for merging files
    """
    with open(data_dir) as input_file:
        obj = json.load(input_file)
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
    def __init__(self, output_path, output_prefix, max_file_size, merger, root_keys):
        self.base = None
        self.output_path = output_path
        self.output_prefix = output_prefix
        self.max_file_size = max_file_size
        self.root_keys = root_keys
        self.merger = merger
        self.counter = 1

    def redundant_obj(self):
        """
        Removes redundant data
        """
        for i in self.root_keys:
            set_of_jsons = {json.dumps(d, sort_keys=False) for d in self.base[i]}
            self.base[i] = [json.loads(t) for t in set_of_jsons]

    def merge_file(self, head, end):
        """
        Merges the files and writes to json file upon reaching limit
        """
        base_size = sizeof(self.base)
        if not end:
            if (base_size < self.max_file_size) and ((base_size+sizeof(head)) <= self.max_file_size):
                self.base = (self.merger).merge(self.base, head)
                #self.redundant_obj()
            else:
                path = os.path.join(self.output_path, '{}{}{}'.format(self.output_prefix, self.counter, '.json'))
                with open(path, 'w', encoding='utf-8') as op:
                    json.dump(self.base, op, ensure_ascii=False)
                self.counter += 1
                self.base = None
                self.base = (self.merger).merge(self.base, head)
        else:
            if self.base:
                path = os.path.join(self.output_path, '{}{}{}'.format(self.output_prefix, self.counter, '.json'))
                with open(path, 'w', encoding='utf-8') as op:
                    json.dump(self.base, op, ensure_ascii=False)

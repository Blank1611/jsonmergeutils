# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 01:58:22 2019

@author: GRENTOR
"""

from genson import SchemaBuilder
def schema_builder(json_object):
    """
    builds schema
    """
    builder = SchemaBuilder()
    builder.add_object(json_object)
    schema = builder.to_schema()
    root_keys = list(schema['properties'].keys())
    for i in root_keys:
        if schema['properties'][i]['type'] == 'array':
            schema['properties'][i]['mergeStrategy'] = "append"
    return schema

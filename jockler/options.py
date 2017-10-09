from jockler import common
from jockler import store
from jockler import files
import os
import json

def read_options(imagename):
    string_data = read_options_file(imagename)

    if not string_data:
        return []
    
    jsondata = json.loads(string_data)
    options = []
    datakeys = jsondata.keys()
    
    for prefix,section in [("-v","volumes"), ("-p", "ports")]:
        if section in datakeys:
            options.extend( expand_as_parameters(prefix, jsondata[section]) )

    return options

def read_options_file(imagename):
    dcvfile = dcv_name(imagename)
    return store.read_data(dcvfile, imagename)

def dcv_name(imagename):
    return "dcv-%s"%imagename

def expand_as_parameters(prefix, datamap):
    params = []
    for datakey in datamap:
        params.extend( [prefix, "%s:%s"%(datakey,datamap[datakey])] )
    return params

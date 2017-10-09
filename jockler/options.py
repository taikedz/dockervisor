from jockler import common
from jockler import store
from jockler import files
import os
import json

def read_options(imagename):
    options = []
    
    for prefix,section in [("-v","volumes"), ("-p", "ports")]:
        options.extend( extract_section(imagename, prefix, section) )

    return options

def extract_section(imagename, prefix, section):
    string_data = read_options_file(imagename)

    if not string_data:
        return []
    
    jsondata = json.loads(string_data)
    options = []
    datakeys = jsondata.keys()

    if section in datakeys:
        options.extend( expand_as_parameters(prefix, jsondata[section]) )

    return options


def read_options_file(imagename):
    jclfile = jcl_name(imagename)
    return store.read_data(jclfile, imagename)

def jcl_name(imagename):
    return "jockler-%s"%imagename

def expand_as_parameters(prefix, datamap):
    params = []
    for datakey in datamap:
        params.extend( [prefix, "%s:%s"%(datakey,datamap[datakey])] )
    return params

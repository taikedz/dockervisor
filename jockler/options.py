import common
import store
import files
import os
import json

def read_options(imagename):
    options = []
    
    for prefix,section in [("-v","volumes"), ("-p", "ports")]:
        options.extend( extract_section(imagename, prefix, section) )

    return options

def json_data(imagename):
    string_data = read_options_file(imagename)

    if not string_data:
        return []

    return json.loads(string_data)

def extract_container_side(imagename, section):
    jsondata = json_data(imagename)
    options = []

    if section in jsondata.keys():
        for k,v in jsondata[section]:
            options.extend( v )

    return options

def extract_section(imagename, prefix, section):
    jsondata = json_data(imagename)
    options = []

    if section in jsondata.keys():
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

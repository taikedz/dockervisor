from dockervisor import common
from dockervisor import store
from dockervisor import files
import os
import json

def setup_options(imagename):
    dcvfile = dcv_name(imagename)
    if not os.path.is_file(dcvfile):
        return

    filedata = files.read_file([dcvfile])
    store.write_data(dcvfile, imagename, filedata)

def read_options_file(imagename):
    dcvfile = dcv_name(imagename)
    return store.read_data(dcvfile, imagename)

def dcv_name(imagename):
    return "dcv-%s"%imagename

def read_options(imagename):
    string_data = read_options_file(imagename)

    if not string_data:
        return []
    
    jsondata = json.loads(string_data)
    options = []
    
    for section in ["volumes", "networks", "ports"]:
        pass # TODO actually load em here

    return options

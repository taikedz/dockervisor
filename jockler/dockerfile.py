from jockler import common
from jockler import files
from jockler import store
from jockler import options
import os
import json
import re

"""
Read the Dockerfile and extract the EXPORT and VOLUMES data
"""

def add_jcl_file(imagename, dockerfile):
    jclfile = options.jcl_name(imagename)
    jcl_data = ""

    if os.path.isfile(jclfile):
        # use local jcl file
        jcl_data = files.read_file([dcvfile])
        jcl_data = json.dumps(json.loads(jcl_data), indent=2)
    else:
        # generate jcl file from dockerfile
        jcl_data = extract_jcl_data(imagename, dockerfile)

    store.write_data(jclfile, imagename, jcl_data)

def extract_jcl_data(imagename, dockerfile_path):
    exposes,volumes = extract_parameters(dockerfile_path)

    jcl_data = {}
    jcl_data["ports"] = {}
    jcl_data["volumes"] = {}

    for exposed_port in exposes:
        jcl_data["ports"][port_number(exposed_port)] = exposed_port

    for mountpoint in volumes:
        jcl_data["volumes"][volume_mount(imagename, mountpoint)] = mountpoint

    return json.dumps(jcl_data, indent=2)

def port_number(portdef):
    m = re.match("([0-9]+)(/(tcp|udp))?", portdef)
    if not m:
        common.fail("Invalid port definition %s"%portdef)
    return m.group(1)

def volume_mount(imagename, mount_path):
    """A deterministic volume name"""
    return "jcl_" + imagename + re.sub("[^a-zA-Z0-9_]+", "_", mount_path)

def extract_parameters(dockerfile_path):
    """ Extract the parameters from the specified dockerfile

    Returns two arrays, the ports to expose, and the volume mount points
    """
    dockerfile_data = read_dockerfile(dockerfile_path)
    return extract_default_parameters(dockerfile_data)

def read_dockerfile(dockerfile_path):
    string_data = files.read_file( dockerfile_path.split(os.path.sep) )
    if not string_data:
        common.fail("Could not find dockerfile [%s]"%dockerfile_path)
    return string_data

def extract_default_parameters(dockerfile_data):
    lines = dockerfile_data.split(os.linesep)

    exposes = find_lines("EXPOSE", lines)
    volumes = find_lines("VOLUME", lines)

    return exposes, volumes

def find_lines(command, lines):
    result = []
    clen = len(command)
    for line in lines:
        if line.startswith(command):
            result.extend( re.split("\\s+", line[clen+1:]) )

    return result

from dockervisor import common
from dockervisor import files
from dockervisor import store
import os
import json

"""
Read the Dockerfile and extract the EXPORT and VOLUMES data
"""

def write_dcv_file(imagename):
    dcvfile = "dcv-%s"%imagename
    dcv_data = ""
    if os.path.isfile(dcvfile):
        dcv_data = files.read_file([dcvfile])
    else:
        dcv_data = extract_dcv_data(imagename, "Dockerfile")

    store.write_data(dcvfile, imagename, dcv_data)
    # TODO is this he right file for this?
    # and should we move this and the read_dcv somewhere?

def extract_dcv_data(imagename, dockerfile_path):
    exposes,volumes = extract_parameters(dockerfile_path)

    dcv_data = {}
    dcv_data["ports"] = {}
    dcv_data["volumes"] = {}

    for exposed_port in exposes:
        dcv_data["ports"][port_number(exposed_port)] = exposed_port

    for mountpoint in volumes:
        dcv_data["volumes"][volume_mount(imagename, mountpoint)] = mountpoint

    return json.dumps(dcv_data)

def port_number(portdef):
    m = re.match("([0-9]+)(/(tcp|udp))")
    if not m:
        return "0"
    return m.group(1)

def volume_mount(imagename, mount_path):
    """A deterministic volume name"""
    return imagename + re.replace("[^a-zA-Z0-9_]+", "_", mount_path)

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
    volumes = find_lines("VOLUMES", lines)

    return exposes, volumes

def find_lines(command, lines):
    result = []
    clen = len(command)
    for line in lines:
        if line.startswith(command):
            result.extend( re.split("\\s+", line[clen+1:]) )

    return result

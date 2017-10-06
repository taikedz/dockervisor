from dockervisor import common
from dockervisor import files
import os

"""
Read the Dockerfile and extract the EXPORT and VOLUMES data
"""

def extract_parameters(imagename, dockerfile_path="Dockerfile"):
    """ Extract the parameters from the specified dockerfile

    Uses imagename for deterministic volume name generation, if applicable
    """
    dockerfile_data = read_dockerfile(dockerfile_path)
    return extract_default_parameters(imagename, dockerfile_data)

def read_dockerfile(dockerfile_path):
    string_data = files.read_file( dockerfile_path.split(os.path.sep) )
    if not string_data:
        common.fail("Could not find dockerfile [%s]"%dockerfile_path)
    return string_data

def extract_default_parameters(imagename, dockerfile_data):
    lines = dockerfile_data.split(os.linesep)

    exposes = find_lines("EXPOSE", lines)
    volumes = find_lines("VOLUMES", lines)

    default_params = []
    default_params.extend( expand_exposes(exposes) )
    default_params.extend( expand_volumes(volumes) )

    return default_params

def expand_volumes(imagename, volumes):
    params = []
    for mount_path in volumes:
        params.extend( ["-v", "%s:%s"%(volume_mount(imagename, mount_path),mount_path)] )
    return params

def expand_exposes(exposes):
    params = []
    for portdef in exposes:
        hostport = port_number(portdef)
        params.extend( ["-p", "%s:%s"%(hostport,portdef)] )
    return params

def port_number(portdef):
    m = re.match("([0-9]+)(/(tcp|udp))")
    if not m:
        return "0"
    return m.group(1)

def volume_mount(imagename, mount_path):
    """A deterministic volume name"""
    return imagename + re.replace("[^a-zA-Z0-9_]+", "_", mount_path)

def find_lines(command, lines):
    result = []
    clen = len(command)
    for line in lines:
        if line.startswith(command):
            result.extend( re.split("\\s+", line[clen+1:]) )

    return result

from dockervisor import store
from dockervisor import common
import os
import re

def build(args):
    imagename = args[0]

    if not re.match("^[a-zA-Z0-9_]+$", imagename):
        common.fail("Image name can only have letters, numbers, and underscore ('_').")

    build_path = common.item(args, 1, ".")

    do_build( imagename, build_path )

def do_build(imagename, build_path):
    print("Building [%s] at [%s] taking files from [%s]" % (imagename, os.path.realpath("Dockerfile"), build_path))
    rescode, stdout, stderr = common.call(''.join( ["docker", "build", "-t", imagename, build_path] ))

    # check stdout for errors

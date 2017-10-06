from dockervisor import store
from dockervisor import common
from dockervisor import run
import os
import re
import sys

def build(args):
    imagename = args[0]

    if not re.match("^[a-zA-Z0-9_]+$", imagename):
        common.fail("Image name can only have letters, numbers, and underscore ('_').")

    build_path = common.item(args, 1, ".")

    res,sout,serr = do_build( imagename, build_path )
    exit(res)

def do_build(imagename, build_path):
    print("Building [%s] at [%s] taking files from [%s]" % (imagename, os.path.realpath("Dockerfile"), build_path))
    rescode, stdout, stderr = run.call(["docker", "build", "-t", imagename, build_path] , stdout=sys.stdout, stderr=sys.stderr)


from dockervisor import store
from dockervisor import common
from dockervisor import run
from dockervisor import dockerfile
import os
import re
import sys
import json

def build(args):
    imagename = args[0]

    if not re.match("^[a-zA-Z0-9_]+$", imagename):
        common.fail("Image name can only have letters, numbers, and underscore ('_').")

    build_path = common.item(args, 1, ".")

    # Add dcv file first - if cannot be generated, prevents build
    add_dcv(imagename)

    res,sout,serr = do_build( imagename, build_path )

    if res == 0:
        image_id = get_tagged_image_id(imagename)
        store.append_data("images", imagename, image_id)

    exit(res)

def add_dcv(imagename):
    try:
        dockerfile.add_dcv_file(imagename)
    except json.JSONDecodeError as e:
        common.fail("Invalid dcv-%s file data:\n%s"%(imagename, str(e)))

def get_tagged_image_id(imagename):
    # This should perform an exact match
    res,sout,serr = run.call(["docker", "images", "--format", "{{.ID}}", imagename], silent=True)

    image_id = sout.strip()
    return image_id

def do_build(imagename, build_path):
    print("Building [%s] at [%s] taking files from [%s]" % (imagename, os.path.realpath("Dockerfile"), build_path))
    return run.call(["docker", "build", "-t", imagename, build_path] , stdout=sys.stdout, stderr=sys.stderr)


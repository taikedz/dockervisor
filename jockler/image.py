from jockler import store
from jockler import common
from jockler import run
from jockler import dockerfile
import os
import re
import sys
import json

def build(args):
    imagename = args[0]

    if not re.match("^[a-zA-Z0-9]+$", imagename):
        common.fail("Image name can only have letters a-z, A-Z and numbers 0-9.")

    build_path = common.item(args, 1, ".")

    # Add jcl file first - if cannot be generated, prevents build
    add_jcl(imagename)

    res,sout,serr = do_build( imagename, build_path )

    if res == 0:
        image_id = get_tagged_image_id(imagename)
        append_image_id(imagename, image_id)

    exit(res)

def add_jcl(imagename):
    try:
        dockerfile.add_jcl_file(imagename)
    except json.JSONDecodeError as e:
        common.fail("Invalid jockler-%s file data:\n%s"%(imagename, str(e)))

def get_tagged_image_id(imagename):
    # This should perform an exact match
    res,sout,serr = run.call(["docker", "images", "--format", "{{.ID}}", imagename], silent=True)

    image_id = sout.strip()
    return image_id

def append_image_id(imagename, image_id):
    imagelist = store.read_data("images", imagename)
    if imagelist == None:
        imagelist = ''
    imagelist = imagelist.split(os.linesep)

    imagelist.append(image_id)
    common.remove_empty_strings(imagelist)
    imagelist = list(set(imagelist))

    store.write_data( "images", imagename, os.linesep.join(imagelist) )

def do_build(imagename, build_path):
    print("Building [%s] at [%s] taking files from [%s]" % (imagename, os.path.realpath("Dockerfile"), build_path))
    return run.call(["docker", "build", "-t", imagename, build_path] , stdout=sys.stdout, stderr=sys.stderr)


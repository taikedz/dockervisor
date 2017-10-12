import store
import options
import common
import run
import dockerfile
import os
import re
import sys
import json

def build(args):
    if not common.args_check(args, 1):
        common.fail("Specify image name to build !")

    imagename = args[0]

    if not re.match("^"+common.imagenamepat+"$", imagename):
        common.fail("Image name can only have letters a-z, A-Z and numbers 0-9.")

    dockerfile, build_path = dockerfiles_for(imagename, args)

    # Add jcl file first - if cannot be generated, prevents build
    add_jcl(imagename, dockerfile)

    res,sout,serr = do_build( imagename, dockerfile, build_path , args[1:])

    if res == 0:
        image_id = get_tagged_image_id(imagename)
        append_image_id(imagename, image_id)

    exit(res)

def dockerfiles_for(imagename, args):
    dockerfile = "%s-Dockerfile"%imagename

    if not os.path.isfile(dockerfile):
        dockerfile = os.path.abspath( common.item(args, 1, "Dockerfile") )

    build_path = os.path.abspath(os.path.join(dockerfile, os.pardir))

    return dockerfile, build_path

def add_jcl(imagename, cdockerfile):
    try:
        dockerfile.add_jcl_file(imagename, cdockerfile)
    except json.JSONDecodeError as e:
        common.fail("Invalid %s file data:\n%s"%(options.jcl_name(imagename), str(e)))

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

def do_build(imagename, dockerfile, build_path, build_args=[]):
    print("Building [%s] at [%s] taking files from [%s]" % (imagename, os.path.realpath(dockerfile), build_path))
    return run.call(["docker", "build", "-t", imagename, "-f", dockerfile] + build_args + [ build_path] , stdout=sys.stdout, stderr=sys.stderr)


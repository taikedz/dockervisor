from dockervisor import store
from dockervisor import common
import os

def build(args):
    imagename = args[0]

    # Check for existing image
    if store.image_defined(imagename):
        build_defined_image(imagename)

    # If none, check for local Dockerfile
    elif os.path.isfile("."+os.path.sep+"Dockerfile"):
        define_and_build_image(args)

    # If none, fail
    else:
        print( "No such image [%s] and no ./Dockerfile" % imagename )
        sys.exit(1)

def build_defined_image(imagename):
    os.chdir(store.image_workdir(imagename) )
    build_path = store.image_build_path(imagename)

    do_build(imagename, build_path)
    print_result(stdout)

def define_and_build_image(args):
    imagename = args[0]

    if lne(args) < 2:
        print("You must specify the directory to pull build files from (usually '.')")
        sys.exit(1)
        
    build_path = args[1]

    if do_build(imagename, build_path)
        store.register( imagename, os.path.realpath("."), build_path )



def do_build(imagename, build_path):
    print("Building [%s] at [%s] taking files from [%s]" % (imagename, os.path.realpath("."), build_path))
    stdout, stderr = common.call(''.join( ["docker", "build", "-t", imagename, build_path] ))

    # check stdout for errors

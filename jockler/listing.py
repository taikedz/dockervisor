from jockler import common
from jockler import run
from jockler import store
from sys import stdout,stderr
import os
import re

helpstr = """

List images and containers

    jockler list { containers | running | images } {IMAGENAME | .all}

List container instance name, or container runtime configuration

    jockler list { last | stable | jcl } IMAGENMAE

"""

def listing(args):
    if not common.args_check(args, 2):
        common.fail(helpstr)

    category = args[0]
    imagename = args[1]

    if imagename == ".all":
        list_all(category)
    else:
        list_on_image(imagename, category)

def ps_filter(imagename):
    return ["--filter", "name=(jcl|dcv)_%s_"%imagename]

def list_on_image(imagename, category):
    psfilter = ps_filter(imagename)

    if category == "containers":
        print_call(["docker", "ps", "-a"]+psfilter)

    elif category == "running":
        print_call(["docker", "ps"]+psfilter)

    elif category == "images":
        # list of images associated with image name
        imagelist = get_image_list_for(imagename)

        # list of all images
        res,sout,serr = run.call(["docker", "images"], silent=True)
        stringlines = sout.strip().split(os.linesep)

        # header
        print("Relevant images: %s" % ', '.join(imagelist) )
        print(stringlines[0])
        # full image line, if image is in imagelist
        for line in filter_string_lines(stringlines, imagelist):
            print(line)

    elif category == "last" or category == "stable":
        print(store.read_data(category, imagename))

    elif category == "jcl":
        print(store.read_data("jockler-%s"%imagename, imagename))

    else:
        unknown_category(category)

def filter_string_lines(stringlines, imagenames):
    result_lines = []
    for imagename in imagenames:
        for stringline in stringlines:
            if imagename in re.split("\\s+", stringline):
                result_lines.append(stringline)
    return result_lines

def get_container_list_for(imagename):
    res,sout,serr = run.call(["docker", "ps", "-a", "--format", "{{.Names}}"] + ps_filter(imagename), silent=True)
    containers = sout.strip().split(os.linesep)
    common.remove_empty_strings(containers)
    return containers

def get_image_of(containername):
    res,sout,serr = run.call(["docker", "ps", "-a", "--format", "{{.Image}}"] + ps_filter(containername), silent=True)
    images = sout.strip().split("\n")

    common.remove_empty_strings(images)

    if len(images) != 1:
        common.fail("Could not find single image for %s"%containername)

    return images[0]
    

def get_image_list_for(imagename):
    #res,sout,serr = run.call(["docker", "ps", "-a", "--format", "{{.Image}}"] + ps_filter(imagename), silent=True)
    #
    #images = sout.strip().split(os.linesep)
    #common.remove_empty_strings(images)
    images = store.read_data("images", imagename)
    if not images:
        return []

    images = list(set(images.split(os.linesep)))

    return images

def image_exists(imagename):
    res, sout, serr = run.call(["docker", "images", "--format", "{{.Repository}}", imagename], silent=True)
    images = sout.strip().split(os.linesep)
    return imagename in images

def unknown_category(category):
    common.fail("Unkown category '%s'; use 'containers', 'running', 'images', or 'stable'")

def print_call(command_array):
    run.call(command_array, stdout=stdout, stderr=stderr)

def list_all(category):
    if category == "containers":
        print_call(["docker", "ps", "-a"])

    elif category == "running":
        print_call(["docker", "ps"])

    elif category == "images":
        print_call(["docker", "images"])

    else:
        unknown_category(category)

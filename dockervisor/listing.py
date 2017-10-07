from dockervisor import common
from dockervisor import run
from sys import stdout
import os

# dockervisor list IMAGE CATCATEGORYY

def listing(args):
    if not common.args_check(args, 2):
        common.fail("Try 'dockervisor {containers|running|images}' IMAGENAME")

    category = args[0]
    imagename = args[1]

    if imagename == ".all":
        list_all(category)
    else:
        list_on_image(imagename, category)

def ps_filter(imagename):
    return ["--filter", "name=%s"%imagename]

def list_on_image(imagename, category):
    psfilter = ps_filter(imagename)

    if category == "containers":
        print_call(["docker", "ps", "-a"]+psfilter)
    elif category == "running":
        print_call(["docker", "ps"]+psfilter)

    elif category == "images":
        imagelist = get_image_list_for(imagename)
        res,sout,serr = run.call(["docker", "images"])
        stringlines = sout.decode("utf-8").strip().split(os.linesep)

        print(stringlines[0])
        for line in filter_string_lines(stringlines, imagelist):
            print(line)
    else:
        unknown_category(category)

def filter_string_lines(stringlines, imagenames):
    result_lines = []
    for imagename in imagenames:
        for stringline in stringlines:
            if imagename in stringline:
                result_lines.append(stringline)
    return result_lines


def get_image_list_for(imagename):
    res,sout,serr = run.call(["docker", "ps", "-a", "--format", "{{.Image}}"] + ps_filter(imagename))
    
    images = sout.decode("utf-8").strip().split(os.linesep)
    images = set(images)

    return images

def unknown_category(category):
    common.fail("Unkown category '%s'; use 'containers', 'running', or 'images'")

def print_call(command_array):
    run.call(command_array, stdout=stdout)

def list_all(category):
    if category == "containers":
        print_call(["docker", "ps", "-a"])
    elif category == "running":
        print_call(["docker", "ps"])
    elif category == "images":
        print_call(["docker", "images"])
    else:
        unknown_category(category)

from dockervisor import common
from dockervisor import run
from dockervisor import image
import re

# dockervisor start {new|last|stable} IMAGE

def start(args):
    if len(args) == 2:
        instance = args[0]
        imagename = args[1]

        if not instance in ["new", "last", "stable"]:
            common.fail("Incorrect instance name. Please use 'new', 'last', or 'stable' ")

        stop_containers(imagename)

        if instance == "new":
            containername = start_new_container(imagename)
        else:
            containername = store.registry_get_instance(instance, imagename)
            if containername:
                start_container(imagename, containername)
            else:
                common.fail("No instance %s for image %s"%(instance, imagename))

    elif len(args) == 1:
        containername = args[0]
        imagename = extract_image_name(containername)
        start_container(imagename, containername)
    
    else:
        # Do not try to implement specifying multiple names in one command
        #   a shell scripter can do that with
        #   for container in name1 name2 name3; do dockervisor start "$container"; done
        common.fail("Unknown. Use 'dockervisor start {new|last|stable} IMAGE' or 'dockervisor start CONTAINER'")

def stop(args):
    if len(args) != 1:
        common.fail("Unknown sequence for stop: %s" % ' '.join(args))

    imagename = args[0]
    stop_containers(imagename)

def remove_empty_strings(string_array):
    while '' in string_array:
        string_array.remove('')

def extract_image_name(containername):
    m = re.match("^dcv_([a-zA-Z0-9_]+)_[0-9]+$", containername)
    if m:
        return m.group(1)
    common.fail("[%s] is not a container managed by dockervisor" % containername)

def get_running_containers(imagename):
    code, sin,sout = run.call(["docker","ps", "--format", "{{.Names}}", "--filter", "name=dcv_%s"%imagename])
    if code > 0:
        common.fail("Could not get list of funning containers")

    containernames = sin.decode("utf-8").strip().split("\n")
    return containernames

def stop_containers(imagename):
    containernames = get_running_containers(imagename)
    remove_empty_strings(containernames)
    if len(containernames) > 0:
        code, sin, sout = run.call( ["docker", "stop"] + containernames )
        if code > 0:
            common.fail("Error stopping container(s) !")

def start_container(imagename, containername):
    store.registry_set_instance("last", imagename, containername)
    code, sin, sout = run.call( ["docker", "start", containername] )
    if code > 0:
        common.fail("Could not start container %s"%containername)

def load_container_options(imagename):
    return [] #TODO

def start_new_container(imagename):
    containername = generate_container_name(imagename)
    options = load_container_options(imagename)
    code, sin, sout = run.call(["docker", "run", "-d", "--name=%s"%containername]+options+[imagename])
    if code > 0:
        common.fail("Could not create new contaienr for %s"%imagename)

    return containername

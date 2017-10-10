from jockler import common
from jockler import run
from jockler import image
from jockler import store
from jockler import options
import re
import time
import sys
import os

# jockler start {new|last|stable} IMAGE [ATTACH]

def start(args):
    if len(args) >= 2:
        instance = args[0]
        imagename = args[1]

        doattach = common.item(args, 2, False)
        if doattach == "attach":
            doattach=True

        if not instance in ["new", "last", "stable"]:
            common.fail("Incorrect instance name. Please use 'new', 'last', or 'stable' ")

        if instance == "new":
            containername = start_new_container(imagename, doattach)
        else:
            containername = store.read_data(instance, imagename)
            if containername:
                start_container(imagename, containername, doattach)
            else:
                common.fail("No instance %s for image %s"%(instance, imagename))

    elif len(args) == 1:
        containername = args[0]
        imagename = extract_image_name(containername)
        if imagename:
            start_container(imagename, containername)
    
    else:
        common.fail("Unknown. Use 'jockler start {new|last|stable} IMAGE' or 'jockler start CONTAINER'")

def stop(args):
    if len(args) != 1:
        common.fail("Unknown sequence for stop: %s" % ' '.join(args))

    imagename = args[0]
    stop_containers(imagename)

def extract_image_name(containername):
    m = re.match("^(jcl|dcv)_([a-zA-Z0-9]+)_[0-9]+$", containername)
    if m:
        return m.group(2)
    common.fail("[%s] is not a container managed by jockler" % containername)

def get_running_containers(imagename):
    code, sout,serr = run.call(["docker","ps", "--format", "{{.Names}}", "--filter", "name=jcl_%s_"%imagename], silent=True)

    containernames = sout.strip().split("\n")
    common.remove_empty_strings(containernames)
    return containernames

def stop_containers(imagename):
    containernames = get_running_containers(imagename)

    if len(containernames) > 0:
        code, sout, serr = run.call( ["docker", "stop"] + containernames )
        if code > 0:
            common.fail("Error stopping container(s) !\n%s"%(sout))

def found_running_container(containername):
    time.sleep(1)
    code, sout, serr = run.call(["docker", "ps", "--format", "{{.Names}}", "--filter", "name=%s"%containername], silent=True)
    containers = sout.strip().split(os.linesep)
    return containername in containers

def load_container_options(imagename):
    coptions = options.read_options(imagename)
    if coptions == None:
        coptions = []
    return coptions

def generate_container_name(imagename):
    datime = common.timestring()
    return "jcl_%s_%s" % (imagename, datime)

def start_container(imagename, containername, doattach=False):
    stop_containers(imagename)
    store.write_data("last", imagename, containername)

    runmode = []
    useexec = False
    if doattach:
        runmode.append("-i")
        useexec = True

    print("Starting %s"%containername)

    code, sout, serr = run.call( ["docker", "start", containername]+runmode, stdout=sys.stdout, stderr=sys.stderr, useexec=useexec )

    if code > 0 or not found_running_container(containername):
        common.fail("Could not start container %s - try starting with 'attach' mode'\n%s"%(containername,sout))

def start_new_container(imagename, doattach=False):
    stop_containers(imagename)
    containername = generate_container_name(imagename)
    options = load_container_options(imagename)

    runmode = "-d"
    useexec = False
    if doattach:
        runmode = "-it"
        useexec = True

    code, sout, serr = run.call(["docker", "run", runmode, "--name=%s"%containername, "--restart", "unless-stopped"]+options+[imagename], useexec=useexec)

    if code > 0 or not found_running_container(containername):
        common.fail("Could not create new container for %s, or could not start created container:\n%s"%(imagename, sout))
    store.write_data("last", imagename, containername)

    return containername

from dockervisor import store
from dockervisor import common
from dockervisor import container

# dockervisor stable IMAGE

helpstr = """
Mark IMAGENAME's currently running container as stable:

    dockervisor stable IMAGENAME

See stable image:

    dockervisor stable :show IMAGENAME

"""

def print_stable_container(imagename):
    containername = store.read_data("stable", imagename)
    if containername:
        print(containername)
    else:
        print("No stable container marked for image [%s]"%imagename)

def mark_stable_container(imagename):

    containernames = container.get_running_containers(imagename)

    if len(containernames) != 1:
        print(containernames)
        common.fail("Could not identify single container to mark as stable")

    containername = containernames[0]

    store.write_data("stable", imagename, containername)

def stable(args):

    if not common.args_check(args, 1):
        common.fail(helpstr)
        
    imagename = args[0]

    if common.args_check(args, 2) and imagename == ":show":
        imagename = args[1]
        print_stable_container(imagename)
    else:
        mark_stable_container(imagename)

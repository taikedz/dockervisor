from dockervisor import store
from dockervisor import common
from dockervisor import container

# dockervisor stable IMAGE

def stable(args):
    if not common.args_check(args, 1):
        common.fail("Insufficient arguments. Run 'docker stable IMAGE' to mark IMAGE's currently running container as stable")
    imagename = args[0]

    containernames = container.get_container_names(imagename)

    if len(containernames) != 1:
        print(containernames)
        common.fail("Could not identify single container to mark as stable")

    containername = containernames[0]

    store.write_data("stable", imagename, containername)

from dockervisor import run
from dockervisor import common
from dockervisor import listing
from dockervisor import store
import sys

# dockervisor remove IMAGENAME

def remove(args, keep_images=[], keep_containers=[]):
    if not common.args_check(args,1):
        common.fail("Remove all containers and images associated with an image.\n\nUsage:\n\n    dockervisor remove IMAGENAME")

    imagename = args[0]

    allimages = listing.get_image_list_for(imagename)
    allcontainers = listing.get_container_list_for(imagename)

    for k in set(keep_containers):
        try_remove(k, allcontainers)
    for k in set(keep_images):
        try_remove(k, allimages)

    if not confirm_removal(allcontainers, allimages):
        common.fail("ABORTED")

    run.call(["docker", "rm"] + allcontainers, stdout=sys.stdout)

    run.call(["docker", "image", "rm"] + list(allimages), stdout=sys.stdout )

def try_remove(item, array):
    try:
        print("Remove %s from %s"%(item, str(array)))
        array.remove(item)
        return True
    except ValueError:
        return False

# remove all old containers and images (not last) (not stable)
def cleanup(args):
    if not common.args_check(args,1):
        common.fail("Remove all old containers and images, except for last and stable.\n\nUsage:\n\n    dockervisor cleanup IMAGENAME")

    imagename = args[0]
    
    keep_images = []
    keep_containers = []

    for instance in ["stable", "last"]:
        container = store.read_data(instance, imagename)
        if container:
            keep_images.append(imagename)
            keep_containers.append(container)

    remove([imagename], keep_images, keep_containers)

def confirm_removal(allcontainers, allimages):
    joiner = ",\n\t"
    print("The following containers will be removed:\n\t%s\n\nThe following images will be removed:\n\t%s\n\n" % (
        joiner.join(allcontainers), joiner.join(allimages)
    ))

    print("Are you sure? y/N> ", end='', flush=True)
    reply = sys.stdin.readline().strip()

    return reply == "y" or reply == "Y"
    

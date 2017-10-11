import run
import common
import listing
import store
import sys

# jockler remove IMAGENAME

def remove(args, keep_images=[], keep_containers=[]):
    if not common.args_check(args,1):
        common.fail("Remove all containers and images associated with an image.\n\nUsage:\n\n    jockler remove IMAGENAME")

    imagename = args[0]

    allimages = listing.get_image_list_for(imagename)
    allcontainers = listing.get_container_list_for(imagename)

    for k in set(keep_containers):
        try_remove(k, allcontainers)
    for k in set(keep_images):
        try_remove(k, allimages)

    if not confirm_removal(allcontainers, allimages):
        common.fail("ABORTED")

    # Remove the image tag
    run.call(["docker","rmi", imagename])

    run.call(["docker", "rm"] + allcontainers, stdout=sys.stdout, silent=True)

    run.call(["docker", "image", "rm"] + allimages, stdout=sys.stdout, silent=True )
    store.cleanup_images(imagename)

def try_remove(item, array):
    try:
        array.remove(item)
        return True
    except ValueError:
        return False

# remove all old containers and images (not last) (not stable)
def cleanup(args):
    if not common.args_check(args,1):
        common.fail("Remove all old containers and images, except for last and stable.\n\nUsage:\n\n    jockler cleanup IMAGENAME")

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
    

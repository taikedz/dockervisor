from dockervisor import common
from dockervisor import listing

# dockervisor remove IMAGENAME

def remove(args):
    if not common.args_check(args,1):
        common.fail("Usage:\n    dockervisor remove IMAGENAME")

    imagename = args[0]
    images = listing.get_image_list_for(imagename)

    # TODO remove all containers
    # remove all images

# remove all old containers and images (not current) (not stable)
def clean(args):
    pass

from dockervisor import store
from dockervisor import common
from dockervisor import container

helpstr = '''

Try the following:

    dockervisor autostart IMAGENAME last
    dockervisor autostart IMAGENAME stable
    dockervisor autostart IMAGENAME none

To start all images marked for autostart:

    dockervisor start-all

'''

startfile = "startup"

def start_all(args):
    image_list = store.list_named_images()

    for imagename in image_list:
        containername = store.read_data(startfile, imagename)
        if not containername or not containername.strip(): # possibly null, or effectively empty string
            continue

        container.start_container(imagename, containername)

def list_start_all():
    image_list = store.list_named_images()

    for imagename in image_list:
        containername = store.read_data(startfile, imagename)
        if not containername or not containername.strip(): # possibly null, or effectively empty string
            continue

        print("%s --> %s"% (imagename, containername.strip() ))

def autostart(args):
    # =================
    # List
    if common.args_check(args, 1):
        common.fail(helpstr)

    if imagename == ":status":
        list_start_all()
        return

    # ==================
    # Mark

    if common.args_check(args, 2):
        common.fail(helpstr)

    imagename = args[0]
    instance = args[1]

    if instance == "none":
        store.write_data(startfile, imagename, "")
    elif instance in ["last", "stable"]:
        store.write_data(startfile, imagename, store.read_data(instance, imagename) )
    else:
        common.fail("Bad instance label [%s]"%instance)

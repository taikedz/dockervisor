from jockler import run
from jockler import store
from jockler import common
from jockler import backup
from jockler import listing
import json
import os
import sys
import time

# list the volumes all containers of a specific image
# should take into account past volumes as well

helpstring = '''
Try one of the following commands:

jockler volumes image IMAGENAME
jockler volumes container IMAGE {last|stable}
jockler volumes backup {windows|linux} IMAGENAME
jockler volumes restore {windows|linux} IMAGENAME ARCHIVEFILE
'''

def volumes(args):
    if not common.args_check(args, 2):
        common.fail(helpstring)
    
    context = args[0]
    imagename = args[1]

    if context == "image":
        imagevolumes = volumes_for(imagename)
        print( os.linesep.join(imagevolumes) )

    elif context == "container":
        instance = "last"
        if common.args_check(args, 3):
            instance = args[2]

        list_container_volumes(imagename, instance)

    elif context == "backup":
        if not common.args_check(args, 3):
            common.fail(helpstring)

        systemname = args[1]
        imagename = args[2]

        backup.do_volume_backup(imagename, systemname)

    elif context == "restore":
        if not common.args_check(args, 4):
            common.fail(helpstring)

        systemname = args[1]
        imagename = args[2]
        archivefile = args[3]

        backup.do_volume_restore(imagename, systemname, archivefile)

    else:
        print(helpstring)
        common.fail("Unknown context [%s]"%context)


def list_container_volumes(imagename, instance):
    if not instance in ["stable", "last"]:
        common.fail("Invalid instance [%s] - use last or stable"%instance)
    
    containername = store.read_data(instance, imagename)
    if not containername:
        common.fail("No candidate [%s] for image [%s]"%(instance,imagename))

    print( os.linesep.join( mountdata_of(containername, "Name") ) )

def mountdata_of(containername, infolabel):
    res, sout, serr = run.call(["docker", "container", "inspect", containername], silent=True)
    inspect_data = json.loads(sout)

    mounts_data = inspect_data[0]["Mounts"]
    infodata = []

    for mountdef in mounts_data:
        infodata.append(mountdef[infolabel])

    return infodata

def volumes_for(imagename):
    """ All the volumes of all the containers presently and previously associated with this image
    """
    all_containers = listing.get_container_list_for(imagename)
    all_volumes = []

    for containername in all_containers:
        all_volumes.extend( mountdata_of(containername, "Name") )

    return list(set(all_volumes))

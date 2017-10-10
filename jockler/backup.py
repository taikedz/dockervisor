import common
import options
import store
import run
import volumes
import os
import sys

# give TGZ of the volumes of an image

# Light oses
lightos = {
    "linux":"alpine",
    "windows":"nanoserver"
}

def do_volume_backup(imagename, systemname, destination="."):
    containername = store.read_data("last", imagename)
    if not containername:
        common.fail("No candidate container for image [%s]"%imagename)

    destination = os.path.abspath(destination)
    mountpoints = volumes.mountdata_of(containername, "Destination")

    archivename = "%s-as-of-%s.tar.gz"%(containername, common.timestring())
    
    if systemname == "linux":
        res, sout, serr = do_linux_volume_backup(containername, destination, archivename, mountpoints)
    elif systemname == "windows":
        #TODO - need a windows version
        common.fail("Not yet implemented")
    else:
        common.fail("Unkown system type [%s]"%systemname)

    if res == 0:
        print("Backup created in %s" % os.path.sep.join([destination, archivename]) )
    else:
        common.fail("Backup operation failed!")

def do_linux_volume_backup(containername, destination, archivename, mountpoints):
    # Load into a basic container
    return run.call(["docker", "run", "--rm", "--volumes-from", containername,
        "-v", "%s:/backup"%destination, lightos["linux"],
        "tar", "cvzf", "/backup/%s"%archivename, "-C", "/"] + mountpoints,
        stdout=sys.stdout, stderr=sys.stderr)

def do_volume_restore(imagename, systemname, archivefile, destination="."):
    destination = os.path.abspath(destination)
    archive_fullpath = os.path.sep.join([destination,archivefile])

    volumes_array = options.extract_section(imagename, "-v", "volumes")

    if not os.path.isfile( archive_fullpath ):
        common.fail("Could not find [%s]"%archive_fullpath)
    
    if systemname == "linux":
        res, sout, serr = do_linux_volume_restore(volumes_array, destination, archivefile)
    elif systemname == "windows":
        #TODO - need a windows version
        common.fail("Not yet implemented")
    else:
        common.fail("Unkown system type [%s]"%systemname)

    if res == 0:
        print("Restore complete from %s" % archivefile)
    else:
        common.fail("Backup operation failed!")

def do_linux_volume_restore(volumes_restore, destination, archivename):
    # Load into a basic container
    return run.call(["docker", "run", "--rm", ] + volumes_restore + [
        "-v", "%s:/backup"%destination, lightos["linux"],
        "tar", "xzvf", "/backup/%s"%archivename, "-C", "/"],
        stdout=sys.stdout, stderr=sys.stderr)

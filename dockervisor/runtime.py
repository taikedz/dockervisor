#!/usr/bin/python3

# Allow runtime to be installed as an executable via symlink

import sys
import os

heredir = os.path.dirname( os.path.realpath(__file__) )
heredir = os.path.realpath( heredir +os.path.sep +"..")
sys.path.append(heredir)

# =======================

from dockervisor import image
from dockervisor import container
from dockervisor import stability
from dockervisor import common
from dockervisor import listing
from dockervisor import removal
from dockervisor import attach
from dockervisor import volumes
from dockervisor import startall

def main():
    if not common.args_check(sys.argv, 2):
        printhelp()
        common.fail("Fail - not enough arguments")
    action = sys.argv[1]

    if action == "build":
        image.build(sys.argv[2:])

    elif action == "start":
        container.start(sys.argv[2:])

    elif action == "stop":
        container.stop(sys.argv[2:])

    elif action == "stable":
        stability.stable(sys.argv[2:])

    elif action == "list":
        listing.listing(sys.argv[2:])

    elif action == "cleanup":
        removal.cleanup(sys.argv[2:])

    elif action == "remove":
        removal.remove(sys.argv[2:])

    elif action == "attach":
        attach.attach(sys.argv[2:])

    elif action == "volumes":
        volumes.volumes(sys.argv[2:])

    elif action == "autostart":
        startall.autostart(sys.argv[2:])

    elif action == "start-all":
        startall.start_all(sys.argv[2:])

    else:
        printhelp()

def printhelp():
    print("""
Dockervisor

Run a container form an image, let dockervisor manage ports, volumes and specific containers.

Build an image from a Dockerfile, and generate port and volume management configs

    dockverisor build IMAGENAME DIRECTORY

Start and stop image containers

    dockervisor start {new|stable|latest} IMAGENAME
    dockervisor stop IMAGENAME

Mark running container as stable

    dockervisor stable IMAGENAME

List containers of an image, associated images, and stable image.

    dockervisor list {containers|running|images|stable} IMAGENAME

Attach to the container of an image

    dockervisor attach IMAGENAME

See volume information

    dockervisor volumes image IMAGENAME
    dockervisor volumes container IMAGENAME

Perform volume backup and restore on 'last' instance

    dockervisor volumes backup {windows|linux} IMAGENAME
    dockervisor volumes restore {windows|linux} IMAGENAME ARCHIVENAME

Remove all containers and images associated with this image name, except for containers and images for last and stable

    dockervisor cleanup IMAGENAME

Remove all data associated with this image !

    dockervisor remove IMAGENAME

Mark an image for automatic starting; use 'none' to turn off autostart

    dockervisor autostart IMAGENAME {last|stable|none}
    dockervisor autostart :status

Start all images marked for autostart:

    dockervisor start-all

    """)

if __name__ == "__main__":
    main()

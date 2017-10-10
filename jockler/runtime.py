#!/usr/bin/python3

# Allow runtime to be installed as an executable via symlink

import sys
import os

heredir = os.path.dirname( os.path.realpath(__file__) )
heredir = os.path.realpath( heredir +os.path.sep +"..")
sys.path.append(heredir)

# =======================

from jockler import image
from jockler import store
from jockler import container
from jockler import stability
from jockler import common
from jockler import listing
from jockler import removal
from jockler import attach
from jockler import volumes
from jockler import startall

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

    elif action == "readme":
        store.dump(["readme.md"])

    else:
        printhelp()

def printhelp():
    print("""
Jockler

Run a container form an image, let jockler manage ports, volumes and specific containers.

Build an image from a Dockerfile, and generate port and volume management configs

    dockverisor build IMAGENAME [DOCKERFILE]

Start and stop image containers

    jockler start {new|stable|latest} IMAGENAME
    jockler stop IMAGENAME

Mark running container as stable

    jockler stable IMAGENAME

List containers of an image, associated images, instance containers, or jockler data.

    jockler list {containers|running|images|stable|last|jcl} {IMAGENAME|.all}

Attach to the container of an image

    jockler attach IMAGENAME

See volume information

    jockler volumes image IMAGENAME
    jockler volumes container IMAGENAME

Perform volume backup and restore on 'last' instance

    jockler volumes backup {windows|linux} IMAGENAME
    jockler volumes restore {windows|linux} IMAGENAME ARCHIVENAME

Remove all containers and images associated with this image name, except for containers and images for last and stable

    jockler cleanup IMAGENAME

Remove all data associated with this image !

    jockler remove IMAGENAME

Mark an image for automatic starting; use 'none' to turn off autostart

    jockler autostart IMAGENAME {last|stable|none}
    jockler autostart :status

Start all images marked for autostart:

    jockler start-all

    """)

if __name__ == "__main__":
    main()

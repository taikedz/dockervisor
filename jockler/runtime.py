#!/usr/bin/python3

# Allow runtime to be installed as an executable via symlink

import sys

# =======================

import image
import store
import container
import stability
import common
import listing
import removal
import attach
import volumes
import readme

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

    elif action == "readme":
        readme.dump(sys.argv[2:])

    else:
        printhelp()

def printhelp():
    print("""
Jockler

Run a container form an image, let jockler manage ports, volumes and specific containers.

Build an image from a Dockerfile, and generate port and volume management configs

    dockverisor build IMAGENAME [DOCKERFILE]

Start and stop image containers

    jockler start {new|stable|latest} IMAGENAME [attach]
    jockler stop IMAGENAME

Force stop containers that are constantly restarting:

    jockler stop -f CONTAINERNAMES ...

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

    """)

if __name__ == "__main__":
    main()

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

    else:
        printhelp()

def printhelp():
    print("""
    Dockervisor

    Run a container form an image, let dockervisor manage ports, volumes and specific containers.

    dockverisor build IMAGENAME DIRECTORY
    dockervisor start [new|stable|latest] IMAGENAME
    dockervisor stop IMAGENAME
    dockervisor stable IMAGENAME
    """)

if __name__ == "__main__":
    main()

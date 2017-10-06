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

def main():
    action = sys.argv[1]

    if action == "build":
        image.build(sys.argv[2:])

    elif action == "start":
        container.start(sys.argv[2:])

    elif action == "stop":
        container.stop(sys.argv[2:])

    elif action == "stable":
        stability.stable(sys.argv[2:])

if __name__ == "__main__":
    main()

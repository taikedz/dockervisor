from jockler import container
from jockler import common
import os

def attach(args):
    if not common.args_check(args, 1):
        common.fail("Usage:\n  jockler attach IMAGENAME [COMMAND]")

    imagename = args[0]

    shellname = "bash"
    if common.args_check(args, 2):
        shellname = args[1]

    containernames = container.get_running_containers(imagename)

    if len(containernames) != 1:
        common.fail("Could not identify single container to attach to:\n%s"%(str(containernames) ))

    command_tokens = ["docker", "exec", "-it", containernames[0], shellname]
    os.execvp(command_tokens[0], command_tokens)

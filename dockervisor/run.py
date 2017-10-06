#!/usr/bin/python

import os
import subprocess

"""
Command runner

Issues commands in the shell
"""

def call(command_tokens):
    """ Runs a command (first token), and resumes python script

    Returns a tuple of (stdout, stderr) output strings
    """
    command = ' '.join(command_tokens)
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    rescode = proc.wait()
    return (rescode, proc.stdout.read(), proc.stderr.read())

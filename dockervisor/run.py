#!/usr/bin/python

import os
import subprocess

"""
Command runner

Issues commands in the shell
"""

def call(command_tokens, stdout=subprocess.PIPE, stderr=subprocess.PIPE):
    """ Runs a command (first token), and resumes python script

    Returns a tuple of (stdout, stderr) output strings
    """
    proc = subprocess.Popen(command_tokens, stdout=stdout, stderr=stderr)
    rescode = proc.wait()

    out_stream = None
    err_stream = None

    if stdout == subprocess.PIPE:
        out_stream = proc.stdout.read()

    if stderr == subprocess.PIPE:
        err_stream = proc.stderr.read()

    return (rescode, out_stream, err_stream)

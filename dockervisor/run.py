#!/usr/bin/python

import os
import subprocess

"""
Command runner

Issues commands in the shell
"""


def call(command_tokens, stdout=subprocess.PIPE, stderr=subprocess.PIPE, silent=False):
    res,sout,serr = call_b(command_tokens, stdout, stderr, silent)

    if sout != None:
        sout = sout.decode("utf-8")

    if serr != None:
        serr = serr.decode("utf-8")

    return res,sout,serr

def call_b(command_tokens, stdout=subprocess.PIPE, stderr=subprocess.PIPE, silent=False):
    """ Runs a command (first token), and resumes python script

    Returns a tuple of (stdout, stderr) output strings
    """
    if not silent:
        print(' '.join(command_tokens))
    proc = subprocess.Popen(command_tokens, stdout=stdout, stderr=stderr)
    rescode = proc.wait()

    out_stream = None
    err_stream = None

    if stdout == subprocess.PIPE:
        out_stream = proc.stdout.read()

    if stderr == subprocess.PIPE:
        err_stream = proc.stderr.read()

    return (rescode, out_stream, err_stream)

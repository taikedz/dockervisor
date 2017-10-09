import sys
import time

def timestring(fmtstring="%Y%m%d%H%M%S"):
    return time.strftime(fmtstring)

def remove_empty_strings(string_array):
    while '' in string_array:
        string_array.remove('')

def args_check(array, minlen):
    return minlen <= len(array)

def item(array, index, defaultv=None):
    if index < len(array):
        return array[index]

    return defaultv

def fail(message, errcode=1):
    print(message)
    sys.exit(errcode)

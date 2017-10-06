import sys

def args_check(array, minlen):
    return minlen <= len(array)

def item(array, index, defaultv=None):
    if index < len(array):
        return array[index]

    return defaultv

def fail(message, errcode=1):
    print(message)
    sys.exit(errcode)

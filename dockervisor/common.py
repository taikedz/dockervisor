from dockshort import run as drun

def args_check(array, minlen):
    return minlen <= len(array)

def fail(message, errcode=1):
    print(message)
    sys.exit(errcode)

def split_on_token(token, array):
    """ Find token and return the two array halves on either side

    If not found, first side is the same array, second side is None
    """
    try:
        i = array.index(token)
        return array[:i], array[i+1:]
    except ValueError as e:
        return array, None

def extract_after_token(token, array):
    """ Find token, return the value after it, and return the found value, and the array with these extracted

    If not found, found value is None, remainder array is same as input
    """
    front, back = split_on_token(token, array)

    if back == None:
        return None, array

    return back[0], front+back[1:]

def rundocker(command, arguments):
    drun.execute(["docker",command]+arguments)

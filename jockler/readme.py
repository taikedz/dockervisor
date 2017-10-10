import store
import common

def dump(args):
    replacement = common.item(args, 0, None)
    readmefile = ["readme.md"]

    sdata = store.load(readmefile)

    if replacement:
        sdata = sdata.replace("MYAPP", replacement)

    print(sdata)

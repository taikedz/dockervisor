import pathlib
from dockervisor import files

# Store dir structure -------------------------
#
# images folder:
# each image should have a corresponding folder
# each folder contains
# * stable - the last item marked stable
# * last - the last instance that was run

homedir = pathlib.Path.home()
a_store_dir = [homedir, "dcv-data"]

def registry_write_file(a_storefile, filedata):
    ''' Ensures the store exists and writes the image data

    Raises IOError if file could not be written or directory could not be created
    '''
    files.ensure_dir(a_storefile[:-1])
    files.write_file(a_storefile, filedata)

def registry_set_instance(instancename, imagename, containername):
    registry_write_file(a_store_dir + [imagename, instancename] , containername )

def registry_read_file(a_storefile):
    ''' Returns the file's dfata, or none if the file is not found
    '''
    return files.read_file(a_storefile)

def registry_get_instance(instancename, imagename):
    return registry_read_file(a_store_dir + [imagename, instancename])
    


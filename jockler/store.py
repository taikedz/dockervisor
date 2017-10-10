from jockler import listing
from jockler import store
import pathlib
import os
from jockler import files

# Store dir structure -------------------------
#
# images folder:
# each image should have a corresponding folder
# each folder contains
# * stable - the last item marked stable
# * last - the last instance that was run

# Support Windows
homedir = str(pathlib.Path.home())
a_store_dir = [homedir, "jockler-data"]

# Unix global path
if os.path.isdir("/var"):
    a_store_dir = ["/var/jockler"]

def dump(path_array):
    data = files.read_file(a_store_dir + path_array)
    if data:
        print(data)
    else:
        print("No [%s]"% os.path.sep.join(path_array))

def write_store_file(a_storefile, filedata):
    ''' Ensures the store exists and writes the image data

    Raises IOError if file could not be written or directory could not be created
    '''
    files.ensure_dir(a_storefile[:-1])
    files.write_file(a_storefile, filedata)

def write_data(filename, imagename, filedata):
    ''' Writes text data to file, overwriting existing data
    '''
    write_store_file(a_store_dir + [imagename, filename] , filedata )

def append_data(filename, imagename, filedata):
    ''' Writes new text data to the end of the file, after a new line
    '''
    olddata = read_data(filename, imagename)
    if olddata:
        filedata = os.linesep.join([olddata,filedata])

    write_data(filename, imagename, filedata )

def read_store_file(a_storefile):
    ''' Returns the file's data, or None if the file is not found
    '''
    return files.read_file(a_storefile)

def read_data(filename, imagename):
    ''' Read text data from file; returns string data, or None if file was not found
    '''
    return read_store_file(a_store_dir + [imagename, filename])

def cleanup_images(imagename):
    imagelist = listing.get_image_list_for(imagename)
    
    for image_id in imagelist:
        if not listing.image_exists(image_id):
            imagelist.remove(image_id)

    store.write_data("images", imagename, os.linesep.join(imagelist) )

def list_named_images():
    dirnames = os.listdir(os.path.sep.join(a_store_dir) )
    valid_dirs = []

    for dirname in dirnames:
        checkpath = os.path.sep.join(a_store_dir + [dirname, "images"])
        if os.path.isfile(checkpath):
            valid_dirs.append(dirname)

    return valid_dirs

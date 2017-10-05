import os
import sys
import pathlib

# Store dir structure -------------------------
# a folder for volumes, and a folder for images
#
# volumes folder:
# (considering tracking which containers volumes have been attached to)
#
# images folder:
# each image should have a corresponding folder
# each folder should have a file "image-meta" stating
#   * workdir
#   * build_path
#   * stable, last and latest container names
# each folder should have a "containers" file containing
#   * a list of the containers created from the image

homedir = pathlib.Path.home()
a_store_dir = [homedir, ".config", "dockervisor"]
a_images_dir = a_store_dir + ["images"]
a_volumes_dir = a_store_dir + ["volumes"]

def ensure_dir(path_array):
    s_path = os.path.sep.join(path_array)
    if not os.path.isdir(s_path):
        os.makedirs(s_path)

def read_file(filepath):
    fh = open(filepath, "r")
    lines = fh.readlines()
    fh.close()

    return ''.join(lines)

def write_file(filepath, filedata):
    fh = open(filepath, "w")
    fh.write(filedata)
    fh.close()

def write_file_def(imagename, filedef):
    a_dirpath = image_conf_dir(imagename)
    ensure_dir(a_dirpath)
    json_data = json.dumps(filedef)

    write_file(os.path.sep.join(a_dirpath+["image-meta"]), json_data)

def read_file_def(imagename)
    metafilepath = os.path.sep.join(image_conf_dir(imagename)+["image-meta"])
    if not os.path.isfile(metafilepath):
        return None

    json_data = read_file(metafilepath)
    filedef = json.loads(json_data)
    return filedef

def image_conf_dir(imagename):
    return a_images_dir + [imagename]

def cleanup():
    # iterate through image folders
    # remove references to images that are no longer present on the system
    # remove references to containers that are no longer present on the system
    # do not use the docker volume prune routine, dangling named volumes can still be re-used
    #    or intriduce an anchor system to always have a container referencing the volumes?
    pass

def register_image(imagename, workdir, build_path):
    fdef = {
        "stable":False,
        "latest": False,
        "last": False,
        "workdir":workdir,
        "build_path":build_path
    }
    write_file_def(imagename, fdef)

def add_container_to_list(imagename, containername):
    a_filepath = a_images_dir + [imagename, "containers"]
    s_content = read_file(a_filepath)
    if not containername in s_content.split("\n"):
        fh = open( os.path.sep.join(a_filepath), "a")
        fh.write("%s\n" % containername)
        fh.close()

def register_container(imagename, containername):
    register_instance(imagename, "last", containername)
    register_instance(imagename, "latest", containername)
    add_container_to_list(imagename, containername)

def register_instance(imagename, instancename, containername):
    fdef = read_file_def(imagename)
    if not fdef:
        return False

    fdef[instancename] = containername

    write_file_def(imagename, fdef)
    return True

def register_last(imagename, containername):
    register_instance(imagename, "last", containername)

def image_defined(imagename):
    if read_file_def(imagename):
        return True
    return False

def image_workdir(imagename):
    fdef = read_file_def(imagename)
    return fdef["workdir"]

def image_build_path(imagename):
    fdef = read_file_def(imagename)
    return fdef["build_path"]

def get_key(keyname, data):

    if not keyname in data.keys():
        print("Bad meta file data - [%s] not defined"%keyname)
        sys.exit(1)

    return data[keyname]

def container_instance(imagename, instance):
    fdef = read_file_def(imagename)
    if not fdef:
        return None

    if instance == ":latest":
        return get_key("latest", fdef)

    elif instance == ":stable":
        return get_key("stable", fdef)

    elif instance == ":last":
        return get_key("last", fdef)
    else:
        raise ArgumentError("Invalid instance name %s" % instance)

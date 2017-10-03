def register_image( imagename, workdir, build_path ):
    pass

def register_container( imagename, containername ):
    # remember to register_last as well
    pass

def register_stable( imagename, containername ):
    pass

def register_latest( imagename, containername ):
    pass

def register_last(imagename, container):
    pass

def image_defined(imagename):
    pass

def image_workdir(imagename):
    pass

def image_build_path(imagename):
    pass

def container_stable(imagename):
    pass

def container_latest(imagenname):
    pass

def container_last_run(imagename):
    pass

def container_instance(imagename, instance):
    if instance == ":latest":
        return container_latest(imagename)
    elif instance == ":stable":
        return container_stable(imagename)
    else:
        raise ArgumentError("Invalid instance name %s" % instance)

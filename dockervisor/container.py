from dockervisor import commmon
from dockervisor import store
from dockervisor import image

def start(args):
    if len(args) == 2:
        imagename = args[0]
        instance = args[1]

        if not instance in [":latest", ":new", ":stable"]:
            common.fail("Incorrect instance name. Please use :latest, :stable or :new ")

        if instance == ":new":
            containername = image.new_container(imagename)
            store.register_container(imagename, containername)
        else:
            containername = store.container_instance(imagename, instance)
            start_container(imagename, containername)

    elif len(args) == 1:
        start_container(imagename, args[0])
    
    else:
        # Do not try to implement specifying multiple names in one command
        #   shell scripter can do that with
        #   for container in name1 name2 name3; do dockervisor start "$container"; done
        common.fail("Unknown sequence for start: %s" % ' '.join(args))

def start_container(imagename, containername):
    store.register_last(imagename, containername)
    common.call( ["docker", "start", containername] )

def stop(args):
    if len(args) != 1:
        common.fail("Unknown sequence for stop: %s" % ' '.join(args))

    imagename = args[0]
    containername = store.container_last_run(imagename)

    if not containername:
        # Could not find a container for the image name
        #   maybe the user passed an actual container name
        containername = imagename

    stop_container(containername)

def stop_container(containername):
    common.call( ["docker", "stop", containername] )

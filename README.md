# Dockervisor

A tool for managing Docker images, containers, and rollback.

## Usage

Dockervisor is intended to be used alongside Dockerfiles.

Running `dockervisor build IMAGENAME .` in the same folder as a Dockerfile creates an image `IMAGENAME`, and adds an override file to `~/dcv/` if a `dcv-$IMAGENAME` file is found in the current directory.

### Creating a new image and container

Install the Dockervisor tool

	git clone https://github.com/taikedz/dockervisor
	sudo dockervisor/install.sh

Switch in to the folder with your Dockerfile, and use dockervisor to build a new image:

	dockervisor build imagename .
	dockervisor start imagename :new

This builds a fresh image to be called `imagename`, and runs a container based off of it. You can pre-supply settings for the container, see *Dockerparams*, below.

You can subsequently run the `dockervisor` command from anywhere to stop/start a container if its image has already been built once.

### Stopping and starting the container

Stop the existing container by image name:

	dockervisor stop imagename

Start the container again:

	dockervisor start imagename :latest

Start a container by name:

	dockervisor start container_name

### Marking stable

You can mark the currently running container as "stable", to indicate that it should be the fallback version

	dockervisor stable mark imagename

You can see which container is marked as stable

	dockervisor stable show imagename

The `:stable` label always points to the same container until explicitly changed.

### Updating the image and container

Simply run the build command against the image name

	dockervisor build imagename

Running `:latest` will still run the previously existing container, we must create a new container which becomes the new latest.

	dockervisor start imagename :new

[preimplementation note: this needs more management than initially thought, since we cannot simply replace an image with one of the same name]

### Rollback

Stop the current container if running, and run your stable version.

	dockervisor stop imagename
	dockervisor start imagename :stable

## Considerations for internal implementation

### Images

The name of the image determines a family of containers. Different images can be created from a same Dockerfile ; as such two Jenkins images could be created from a same Dockerfile and have a separate family of containers each.

This does create image duplication, however it eases container management separation.

Images rebuilt with the same name leave their old image behind as an unnamed image for the original containers to continue using.

### Containers

* containers get named as `dcv_$IMAGENAME` upon creation
* marking as stable makes the image get renamed to `dcv_$IMAGENAME_stable`
* containers being otherwise renamed get `$dcv_$IMAGENAME_save_$DATETIME`

### Volumes

We can use the EXPOSE directives to generate volumes based on image name and path

Every time a new container is created from a same image, it inherits the same voluimes as its predecessor

For example, for an image created as "mainjenkins" and exposing a mount location of `/var/jenkins_home`, a volume called `mainjenkins_var_jenkins_home` is created. Any container created from the `mainjenkins` image will receive the same named volume.

### Ports

Ports get mapped out one-to-one by default - for example, if the Dockerfile specifies `EXPOSE 8080`, then a mapping `-p 8080:8080` is added.

## Dockerparams

An application definition `$dcv-$IMAGENAME` in your current working directory is a JSON file specifying container runtime parameters for network, port exposure, and volume mounting; this is only used on creation of a new container.

To start a container with the preconfigured parameters, run

	dockervisor start IMAGENAME :new CONFIGNAME

With `configname` being the name of the configuration in the Dockerparams file.

The top level object is a has map, containing the individual configuration objectss.

Each individual configuration object referenced by name can have the following properties:

* `volumes` - a map of `volume-or-path --> /container/mount/point`
* `ports` - a map of ports to expose `host-port --> container-port`
* `networks` - a list of networks to connect to - see the man page for docker(1), the entry on `--network=` option

Some addiitonal entries

* `raw` - a list of raw parameters to pass to docker-run
* `arguments` - a list of arguments to be passed to the container
* `env` - a map of environment variables

For example, the following is a possible definition for a wordpress site, with an internal database instance, and exposing on the host's port `80`

	{
		"volumes" : {
			"mysqldata" : "/usr/share/mysql",
			"./logs/mysql" : "/var/log/mysql"
		},
		"networks" : ["named_network"],
		"ports": {
			"3306" : "3306"
		}
	}

Another definition could contain

	{
		"networks" : ["bridge", "named_network"],
		"volumes" : {
			"wpdata" : "/var/www/html",
			"./logs/apache" : "/var/log/apache2"
		},
		"ports" : {
			"80" : "80"
		},
		"env" : { "WPDATABASE" : "thedatabase" }
	}

You would then be able to

* run `dockervisor build ...` for your images
* then sequentially run `dockervisor start $imagename :new $configname` with the `Dockerparams` file in your curent working direcotry

# extra notes

`shell_reference` is an example implementation for a tool that I wrote in bash

In doing so, I realized that container and image name management could be more dynamic than I thoguht

I also found that alternate dockerfiles can be speicifed on command line, as well as explored auto-generating volume names and port exposure

This is something that can be added to the dockervisor

It should also be possible to simplify the container management, and perhaps remove the need for the store

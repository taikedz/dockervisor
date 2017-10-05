# Dockervisor

A tool for managing Docker images, containers, and rollback.

(incomplete)
(I thikn I waterfalled it and went down a rabbit hole...)

## Usage

Dockervisor is intended to be used on Dockerfiles.

Running `dockervisor build APPNAME .` in the same folder as a Dockerfile registers `APPNAME` in dockervisor's list of apps against the path to the dockerfile, and allows subsequent management of images and containers.

### Creating a new image and container

Install the Dockervisor tool

	git clone https://github.com/taikedz/dockervisor
	sudo dockervisor/install.sh

Switch in to the folder with your Dockerfile, and use dockervisor to build a new image:

	dockervisor build myapp .
	dockervisor start myapp :new

This builds a fresh image to be called `myapp`, and runs a container based off of it. You can pre-supply settings for the container, see *Dockerparams*, below.

You can subsequently run the `dockervisor` command from anywhere to stop/start a container if its image has already been built once.

### Stopping and starting the container

Stop the existing container by image name:

	dockervisor stop myapp

Start the container again:

	dockervisor start myapp :latest

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

	dockervisor build myapp

Running `:latest` will still run the previously existing container, we must create a new container which becomes the new latest.

	dockervisor start myapp :new

[preimplementation note: this needs more management than initially thought, since we cannot simply replace an image with one of the same name]

### Rollback

Stop the current container if running, and run your stable version.

	dockervisor stop myapp
	dockervisor start myapp :stable

## Dockerparams

_NOTE -- this is a wishlist item at this time, and is subject to change or cancellation_

An application definition `Dockerparams` in your current working directory is a JSON file specifying container runtime parameters for network, port exposure, and volume mounting; this is only used on creation of a new container.

To start a container with the preconfigured parameters, run

	dockervisor start APP :new CONFIGNAME

With `configname` being the name of the configuration in the Dockerparams file.

The top level object is a has map, containing the individual configuration objectss.

Each individual configuration object referenced by name can have the following properties:

* `volumes` - a map of `volume-or-path --> /container/mount/point`
* `ports` - a map of ports to expose `host-port --> container-port`
* `networks` - a list of networks to connect to - see the man page for docker(1), the entry on `--network=` option
* `raw` - a list of raw parameters to pass to docker-run
* `arguments` - a list of arguments to be passed to the container
* `env` - a map of environment variables

For example, the following is a possible definition for a wordpress site, with an internal database instance, and exposing on the host's port `80`

	{
		"thedatabase" : {
			"volumes" : {
				"mysqldata" : "/usr/share/mysql",
				"./logs/mysql" : "/var/log/mysql"
			},
			"networks" : ["named_network"],
			"ports": {
				"3306" : "3306"
			}
		},

		"apache" : {
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
	}

You would then be able to

* run `dockervisor build ...` for your images
* then sequentially run `dockervisor start $imagename :new $configname` with the `Dockerparams` file in your curent working direcotry

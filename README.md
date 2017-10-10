# Jockler

A tool to juggle Docker images and containers so You don't have to.

Written to allow non-docker-fluent admins to manage docker containers and image upgrades easily.

Here's an [example readme](example-readme.md) that can be given to basic maintenance admins, for apps managed by jockler (also accessible any time via `jockler readme`).

## Features

* start/stop latest container using the image name - let jockler manage container instances
* mark a given container as "stable" - rollback to a "stable" version after running a new container, if needed
* ensure every container for a given image uses the same data volumes
* backup and restore volume data (Linux only for now) across hosts
* automatically clean out old, unused containers and images
* automatically start select containers on machine boot-up (requires systemd)

Jockler allows you to start and stop containers by specifying the image name, instead of individual container names. Any one image managed by jockler can only have one container running.

Jockler ensures that all containers started by jockler use the same port exposures and volume mounts, using a `jockler-$IMAGENAME` file.

This means that if you build a new version of an image, your new container will use the same data as the old container.

## Pre-requisites

Required:

* Jockler is implemented in Python 3
* You will need the latest docker-ce: see the [official docker documentation](https://www.docker.com/community-edition)

Optional:

* `git` is required for cloning, or you can download a [ZIP file](https://github.com/taikedz/jockler/archive/master.zip)
* For auto-start functionality, systemd is required, or you will need to write your own init script

Install the Jockler tool:

	git clone https://github.com/taikedz/jockler
	sudo jockler/install.sh

	# Optionally, enable autostart
	sudo systemctl enable jockler-autostart

If your system does not use systemd, you will need to write your own init script to call `jockler start-all` on system startup

## Quickstart

In a directory with a Dockerfile, build the image, and register its port exposures and volume mounts to the jockler store. If the image already existed, it is replaced with a newer version.

	jockler build IMAGENAME

Start a fresh container from the image - this always creates a new container and starts it, even if others had previously been created. Port exposures and volume mounts are pulled from jockler store.

	jockler start new IMAGENAME

Stop the container

	jockler stop IMAGENAME

Start the last used container from that image

	jockler start last IMAGENAME

Mark the currently running container as stable - one you might want to come back to after upgrading an image

	jockler stable IMAGENAME

Start the last known stable container

	jockler start stable IMAGENAME

List images (present and past) associated with IMAGENAME

	jockler list images IMAGENAME

Backup your data

	jockler volumes backup linux IMAGENAME

Restore your data

	jockler volumes restore linux IMAGENAME ARCHIVEFILE

## Usage

### Jockler store

Jockler stores its metadata on image and containers in `/var/jockler` on Linux, `%HOME%/jockler-data` on Windows.

### Creating a new image and container

Switch in to the folder with your Dockerfile, and use jockler to build a new image:

	jockler build IMAGENAME [DOCKERFILE]
	jockler start new IMAGENAME

By default, jockler will look for a `$IMAGENAME-Dockerfile` file in the current working directory. If this is not found, it will use the default `./Dockerfile`. Explicitly specifying a DOCKERFILE overrides this behaviour.

Jockler will also look for a `jockler-$IMAGENAME` file to register port mappings and volumes; if none is found, port and volume information are taken from the dockerfile.

This builds a fresh image to be called `IMAGENAME`, and runs a container based off of it.

You can subsequently run the `jockler` command from anywhere to stop/start a container if its image has already been built once.

### Stopping and starting the container

Stop the existing container by image name:

	jockler stop IMAGENAME

Start the container again:

	jockler start last IMAGENAME

Start a container by name - the container must be of the format `jcl_$IMAGENAME_$SUFFIX`:

	jockler start container_name

### Marking stable

You can mark the currently running container as "stable", to indicate that it should be the fallback version

	jockler stable mark IMAGENAME

You can start the registered stable container by running

	jockler start stable IMAGENAME

You can see which container is marked as stable

	jockler stable show IMAGENAME

The `stable` label always points to the same container until explicitly changed.

### Updating the image and container

Simply run the build command against the image name

	jockler build IMAGENAME .

Running `last` will still run the previously existing container, we must create a new container which becomes the new last.

	jockler start new IMAGENAME

### Rollback

Run your stable version - this will also stop any currently running version.

	jockler start stable IMAGENAME

### Auto-start

Jockler can mark images for automatic starting:

	jockler autostart IMAGENAME {last|stable|none}

If not set, or set to none, the image's container will not be started

To see the current status of all images

	jockler autostart :status

To run all containers marked for autostart, run

	jockler start-all

To have this run at host startup, run

	systemctl enable jockler-autostart

This is only available on systems with systemd.

### Backup and restore

You can create .TAR.GZ backup files of a `last` container of an image

	jockler volumes backup linux IMAGENAME
	jockler volumes restore linux IMAGENAME ARCHIVENAME

You need to specify `linux` for Linux-based containers ; support for Windows-based containers will eventually be added.

Before restoring, you need an equivalent image definition - if you are moving to another host, using the same dockerfile and optional remapping file, you can execute the following sequence:

	jockler build IMAGENAME DIRECTORY
	jockler volumes restore linux IMAGENAME ARCHIVENAME
	jockler start new IMAGENAME

### Deletion

You can have jockler remove all containers and images associated with an image name with these commands:

	jockler cleanup IMAGENAME
	jockler remove IMAGENAME

The `cleanup` operation does not remove the last container run, and does not remove the `stable` container; it also does not remove the images associated with these. All other containers and images associated with this image name are removed.

The `remove` operation removes ALL containers and images associated with this image name.

Both prompt you once before execution.

## Implementation specifics

### Images

The name of the image determines a family of containers. Different images can be created from a same Dockerfile ; as such two apache images could be created from a same Dockerfile and have a separate family of containers each.

This does create image duplication, however it eases container management separation.

Images rebuilt with the same name leave their old image behind as an unnamed image for the original containers to continue using.

You can use `jockler list images IMAGENAME` to list all images associated with that name.

### Containers

Containers get named as `jcl_$IMAGENAME_$DATE` upon creation.

Jockler keeps track of which was last run, and which is marked as stable.

### Volumes

Jockler uses the `VOLUME` directives from the Dockerfile to generate volumes based on image name and path, unless overridden (see Remapping section).

Every time a new container is created from a same image, it inherits the same volumes as its predecessor, since the volume name is generated deterministically.

For example, for an image created as `mainapache` and exposing a mount location of `/var/www`, a volume called `jcl_mainapache_var_www` is created. Any container created from the `mainapache` image will receive the same named volume.

### Ports

Jockler uses the `EXPORT` directives from the Dockerfile to generate port exposure mappings, unless overridden (see Remapping section).

Ports get mapped out one-to-one by default - for example, if the Dockerfile specifies `EXPOSE 8080`, then a mapping `-p 8080:8080` is used.

## Remapping

A remapping overrides file can be specified to override the ports: add a `jockler-$IMAGENAME` to the same directory as the Dockerfile containing a JSON data file with the appropriate keys.

Multiple keys can be used (once per key name) in the same overrides file.

### Ports

Use a "ports" key using a map of `host port --> container port definition`

for example, to expose the container's port `8080` on the host's port `80`, and the container's port `22` on the host's port `8022`

	{
		"ports": {
			"80":"8080/tcp",
			"8022":"22"
		}
	}

You can optionally specify the transport `/tcp` or `/udp` after the container port.

### Volumes

Use a "volumes" key using a map of `host path or volume --> container mount point`

for example, to mount `my_custom_volume` on `/var/data`:

	{
		"volumes": {
			"my_custom_volume":"/var/data"
		}
	}

The host portion can be a directory, or a docker volume

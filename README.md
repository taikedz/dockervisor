# Dockervisor

A tool for managing Docker images, containers, and rollback.

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

This builds a fresh image to be called `myapp`, and runs a container based off of it.

You can subsequently run the `dockervisor` command from anywhere to stop/start a container if its image has already been built once.

### Stopping and starting the container

Stop the existing container by image name:

	dockervisor stop myapp

Start the container again:

	dockervisor start myapp :latest

Start a container by name:

	dockervisor start container_name

## Marking stable

You can mark the currently running container as "stable", to indicate that it should be the fallback version

	dockervisor stable mark

You can see which container is marked as stable

	dockervisor stable show

The `:stable` label always points to the same container until explicitly changed.

## Updating the image and container

Simply run the build command against the image name

	dockervisor build myapp

Running `:latest` will still run the previously existing container, we must create a new container which becomes the new latest.

	dockervisor start myapp :new

## Rollback

Stop the current container if running, and run your stable version.

	dockervisor stop myapp
	dockervisor start myapp :stable

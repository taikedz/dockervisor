# MYAPP base image

For ease of maintenance, we use [jockler](https://github.com/taikedz/jockler) instead of bare docker commands.

## Setup

	jockler build MYAPP

## Start

	jockler start new MYAPP

## Upgrade

Mark the current running container as stable, then upgrade the MYAPP image:

	jockler stable MYAPP
	jockler build MYAPP
	jockler start new MYAPP

If for any reason you need to roll back to the stable version, run

	jockler start stable MYAPP

## Backup

Take a backup of MYAPP's volumes - this will create a `.tar.gz` file of the data - you should consider stopping the container before performing the backup, to avoid inconsistent-data corruption

	jockler stop MYAPP
	jockler volumes backup linux MYAPP
	jockler start last MYAPP

Restore the data:

	jockler volumes restore linux MYAPP ARCHIVEFILE

## Maintenance

If after a while you find that you have a lot of images and containers lying around on disk, you can run a cleanup to remove all images and containers, except the stable container, the last-run container, and their respective images.

	jockler cleanup MYAPP

## Issues

If a container can't start, it might get stuck in a "Restarting" loop

Stop such containers:

	jockler stop -f CONTAINERNAMES ...

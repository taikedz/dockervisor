#!/bin/bash

set -eu

cd "$(dirname "$0")"

[[ "$UID" = 0 ]] || {
	echo "You must be root to run this script"
	exit 1
}

if ! grep -q -e '^docker:' /etc/group; then
	echo "Could not find docker group on this system - abort."
	exit 1
fi

DOCKERVISOR_DIR="/usr/share/dockervisor"
DOCKERVISOR_EXE="/usr/bin/dockervisor"
DOCKERVISOR_DAT="/var/dockervisor"

if [[ -d "$DOCKERVISOR_DIR" ]]; then
	echo "Removing existing dockervisor ..."
	rm -r "$DOCKERVISOR_DIR"
fi

echo "Copying dockervisor to $DOCKERVISOR_DIR..."
cp -r dockervisor "$DOCKERVISOR_DIR"
chmod -R 644 "$DOCKERVISOR_DIR"
chmod 755 "$DOCKERVISOR_DIR" "$DOCKERVISOR_DIR/runtime.py"

if [[ -h "$DOCKERVISOR_EXE" ]]; then
	echo "Unlinking old dockervisor command ..."
	unlink "$DOCKERVISOR_EXE"
fi

echo "Installing new dockervisor ..."
ln -s "$DOCKERVISOR_DIR/runtime.py" "$DOCKERVISOR_EXE"

if [[ ! -d "$DOCKERVISOR_DAT" ]]; then
	echo "Creating dockervisor data dir in $DOCKERVISOR_DAT"
	mkdir "$DOCKERVISOR_DAT"
	chown :docker "$DOCKERVISOR_DAT"
	chmod 775 "$DOCKERVISOR_DAT"
fi

echo "Finished."

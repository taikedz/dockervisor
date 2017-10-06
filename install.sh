#!/bin/bash

set -eu

cd "$(dirname "$0")"

[[ "$UID" = 0 ]] || {
	echo "You must be root to run this script"
	exit 1
}

DOCKERVISOR_DIR="/usr/share/dockervisor"
DOCKERVISOR_EXE="/usr/bin/dockervisor"

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

echo "Finished."

#!/bin/bash

set -eu

cd "$(dirname "$0")"

# ==========================================
# Pre-flight check

[[ "$UID" = 0 ]] || {
	echo "You must be root to run this script"
	exit 1
}

if ! grep -q -e '^docker:' /etc/group; then
	echo "Could not find docker group on this system - abort."
	exit 1
fi

JOCKLER_DIR="/usr/share/jockler"
JOCKLER_EXE="/usr/bin/jockler"
JOCKLER_DAT="/var/jockler"
JOCKLER_SER="/etc/systemd/system/jockler-autostart.service"

# ==========================================
# Remove old versions to avoid file conflicts

if [[ -d "$JOCKLER_DIR" ]]; then
	echo "Removing existing jockler ..."
	rm -r "$JOCKLER_DIR"
fi

echo "Copying jockler to $JOCKLER_DIR..."
cp -r jockler "$JOCKLER_DIR"
chmod -R 644 "$JOCKLER_DIR"
chmod 755 "$JOCKLER_DIR" "$JOCKLER_DIR/runtime.py"


# ==========================================
# In case we changed the location of the executable

if [[ -h "$JOCKLER_EXE" ]]; then
	echo "Unlinking old jockler command ..."
	unlink "$JOCKLER_EXE"
fi

echo "Installing new jockler ..."
cp bin/jockler "$JOCKLER_EXE"
chmod 755 "$JOCKLER_EXE"


# ==========================================
# Service file ; also check to see that destination exists
# in lieu of checking for systemctl itself

if [[ -f "$JOCKLER_SER" ]]; then
	echo "Replacing service file"
	rm "$JOCKLER_SER"
fi

if [[ -d "$(dirname "$JOCKLER_SER")" ]]; then
	echo "Installing new service file"
	cp service/jockler.service "$JOCKLER_SER"
fi


# ==========================================
# Data ; this is the Linux install script
# no Windows support

if [[ ! -d "$JOCKLER_DAT" ]]; then
	echo "Creating jockler data dir in $JOCKLER_DAT"
	mkdir "$JOCKLER_DAT"
	chown :docker "$JOCKLER_DAT"
	chmod 775 "$JOCKLER_DAT"
fi

cp -i example-readme.md "$JOCKLER_DAT/readme.md" && chown :docker "$JOCKLER_DAT/readme.md"

echo "---- Finished ----"

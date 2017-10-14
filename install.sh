#!/bin/bash

set -eu

cd "$(dirname "$0")"

JOCKLER_DIR="/usr/share/jockler"
JOCKLER_EXE="/usr/bin/jockler"
JOCKLER_DAT="/var/jockler"
JOCKLER_SER="/etc/systemd/system/jockler-autostart.service"

# ==========================================
# Pre-flight check

precheck() {
	[[ "$UID" = 0 ]] || {
		echo "You must be root to run this script"
		exit 1
	}

	if ! grep -q -e '^docker:' /etc/group; then
		echo "Could not find docker group on this system - abort."
		exit 1
	fi
}

# ==========================================
# Remove old versions to avoid file conflicts

add_jockler_assets() {
	if [[ -d "$JOCKLER_DIR" ]]; then
		echo "Removing existing jockler ..."
		rm -r "$JOCKLER_DIR"
	fi

	echo "Copying jockler to $JOCKLER_DIR..."
	cp -r jockler "$JOCKLER_DIR"
	chmod -R 644 "$JOCKLER_DIR"
	chmod 755 "$JOCKLER_DIR" "$JOCKLER_DIR/runtime.py"
}

# ==========================================
# In case we changed the location of the executable

link_jockler_exe() {
	if [[ -h "$JOCKLER_EXE" ]]; then
		echo "Unlinking old jockler command ..."
		unlink "$JOCKLER_EXE"
	fi

	echo "Installing new jockler ..."
	cp assets/bin/jockler "$JOCKLER_EXE"
	chmod 755 "$JOCKLER_EXE"
}


# ==========================================
# Data ; this is the Linux install script
# no Windows support

add_jockler_config_dir() {
	if [[ ! -d "$JOCKLER_DAT" ]]; then
		echo "Creating jockler data dir in $JOCKLER_DAT"
		mkdir "$JOCKLER_DAT"
		chown :docker "$JOCKLER_DAT"
		chmod 775 "$JOCKLER_DAT"
	fi
}

add_new_readme() {
	if [[ ! -f "$JOCKLER_DAT/readme.md" ]]; then
		cp assets/example-readme.md "$JOCKLER_DAT/readme.md" && chown :docker "$JOCKLER_DAT/readme.md"
	fi
}

main() {
	precheck
	add_jockler_assets
	link_jockler_exe
	add_jockler_config_dir
	add_new_readme

	echo "---- Finished ----"
}

main "$@"

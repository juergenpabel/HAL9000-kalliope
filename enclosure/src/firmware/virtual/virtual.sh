#!/bin/bash

trap cleanup SIGINT
cleanup() {
	echo "Removing (virtual) device sockets..."
	screen -q -XS virtual-hal9000:socat quit 2>&1 >/dev/null

	echo "Done."
	exit 0
}

DEVICE="/dev/ttyHAL9000"
if [[ "x$1" != "x" ]]; then
	DEVICE="$1"
fi

echo "Creating (virtual) device sockets..."
if [[ -e "${DEVICE}" ||  -e "${DEVICE}.virtual" ]]; then
	echo "At least one of the devices ('${DEVICE}', '${DEVICE}.virtual') already exists, exiting."
	exit 0
fi
screen -dmS virtual-hal9000:socat socat -d -d pty,raw,echo=0,link="${DEVICE}" pty,raw,echo=0,link="${DEVICE}.virtual"
sleep 1
if [[ ! -L "${DEVICE}" ||  ! -L "${DEVICE}.virtual" ]]; then
	echo "At least one of the devices ('${DEVICE}', '${DEVICE}.virtual') could not be created (probably a /dev permissions issue, use /tmp/... instead), exiting."
	screen -q -XS virtual-hal9000:socat quit 2>&1 >/dev/null
	exit 0
fi


echo "Running virtual firmware, bound to '${DEVICE}.virtual' (use '${DEVICE}' as device)..."
python3 virtual.py "${DEVICE}.virtual"
cleanup



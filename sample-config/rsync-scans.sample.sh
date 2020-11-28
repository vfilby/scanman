#!/bin/sh

# This assumes you the host you are sending scans to has ssh and an appropriate known_key
# configuration. See how to setup passwordless ssh for this to work.
#
# Once you have this script working you can run it regularly (every minute) via cron:
#
# * * * * *             cd /path/to/scans && /path/to/rsync-scans.sh

# sync any scans removing them after they are synchronized
flock -n /path/to/scans -c "rsync --remove-source-files -rtP -e 'ssh -i <your key file> -p <port>' . <user>@<ip>:<path>"

# clean up any empty directories left behind by rsync
find . -depth -type d -empty -delete

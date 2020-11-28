#!/bin/sh

TMP_DIR=$(mktemp -d -p "" scan.XXXXXXXXXX)
SCAN_NAME=`date +"scan - %Y-%m-%d - %Y%m%d%H%M"`
SCAN_DIR="/path/to/scans/$SCAN_NAME"

echo "scan.sh: Scanning..."
sudo scanadf -d fujitsu --resolution 300 --mode Color --source "ADF Duplex" -o $TMP_DIR/scan-%04d
echo "scan.sh: generating file_manifest"
cd $TMP_DIR && shasum -a 1 scan-* > file_manifest
chmod 755 $TMP_DIR
echo "scan.sh: Moving $TMP_DIR to \"$SCAN_DIR\""
mv $TMP_DIR "$SCAN_DIR"
echo "scan.sh: Done"

#!/bin/sh

TMP_DIR=$(mktemp -d -p "" scan.XXXXXXXXXX)
SCAN_NAME=`date +"scan - %Y-%m-%d - %Y%m%d%H%M%S"`
SCAN_DIR="/home/scans/$SCAN_NAME"
DEVICE=fujitsu
RESOLUTION=300
MODE=Color
PAGE_HEIGHT=500mm

echo "scan.sh: Scanning..."
sudo scanadf -d fujitsu --resolution $RESOLUTION --mode $MODE --source "ADF Duplex" -o $TMP_DIR/scan-%04d --page-height=$PAGE_HEIGHT --buffermode=On --swcrop=yes
echo "scan.sh: generating file_manifest"
cd $TMP_DIR && shasum -a 1 scan-* > file_manifest
chmod 755 $TMP_DIR
echo "scan.sh: Moving $TMP_DIR to \"$SCAN_DIR\""
mv $TMP_DIR "$SCAN_DIR"
echo "scan.sh: Done"

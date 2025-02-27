## Summary

I was looking for a way to untether my Fujitsu ix500 from a laptop to make it a general networked scanner that would create searchable .pdf's and leave them on a network share.  Originally I tried running this solely on a Raspberry Pi (like [this](https://chrisschuld.com/2020/01/network-scanner-with-scansnap-and-raspberry-pi/)) but this was prohibitively slow.  Even on the Pi 4 it could easily take more than 30 minutes to assemble and run OCR.  Which leads me to this two part solution: 1) a raspberry pi that is connected to the scanner that collects scans and sends them to another hose, and 2) a process running on the host that would watch for new scans and process them.

## Detailed Flow

**Part 1: Scanning**

All of this happens on a Raspberry Pi attached to scanner via USB

1. `scanbd` runs on the Pi and runs a script to collect the files.
2. The script puts the raw data from sane into a directory and creates a file manifest with a cryptographic hash for each file.
3. This folder is then placed in a general dropbox which can be sent, sync'd or pulled to the other computer.

**Part 2: Processing**

1. The `scanman` python script will watch a directory and look for any subdirectory that contains a `file_manifest`.
2. For every directory that contains a `file_manifest` it will verify the cryptographic hashes for each file.  It does so to ensure that the transfer is complete before processing.  If the check fails, it will skip it and try again on the next poll.
3. If the files can be verified the script will combine the images with `img2pdf` and make it searchable with `ocrmypdf`
4. Once the .pdf is complete it will move the file to a `completed directory` and delete the source image files

Note that you can completely bypass the OCR stage by setting the environment variable COMBINE_ONLY to "True".  This is useful if you plan on using a 
more complex system downstream like paperless-ngx.

## Development

**Dependencies**

*Docker* If you plan to use docker, you really only need docker.  All the dependencies should be pulled in when you create the docker image.

*Local* If you plan on running it locally you will need some dependencies installed.  See the Dockerfile for a list of packages you need to install.

`RUN apt-get update && apt-get install -y --no-install-recommends \
  netpbm \
  ghostscript \
  poppler-utils \
  imagemagick \
  unpaper \
  util-linux \
  tesseract-ocr \
  parallel \
  units \
  ssh \
  git \
  vim \
  bash \
  bc`


To manage the python packages/env you will need to use pipenv (or really just go rogue, it's a choice).  `pipenv shell` will create the virtualenv and/or activate it for you.  `pipenv install --dev` will install all the libraries/packages you need.


**Running it**

The included makefile has options for local or docker based dev.  

`make local-run` will run the python script in your host environment
`make docker-run` will create a docker image and run the python script

See the `Makefile` for more details.

## Known Glitches/Problems

* If the scanner jams scanbd will turn the light orange and stop scanning.  On the fujitsu I need to close and reopen the lid (essentially turn it off and on).  Not terrible but the partial scan will be saved and treated as if it is a full scan.
* Oversized paper will not work (long receipts, etc). NOTE: This is kinda resolved, by setting a large paper height and swcrop (at least with the Fujitsu scanner) this seems to work, but slows the scanning process slightly.  sample scan script has been updated.


## Things that would be nice to add

* add buttons to support different modes colour, greyscale, etc.
* colour/BW auto detection. (Maybe convert from colour to greyscale in the processing?)
* automatically crop out white edges, currently recents are scanned as full sheets
* attempt to detect the title/date for naming
* add on error notification hooks
* Add a queue cleared notification.

## Resources

* Managing python versions on ubuntu: https://hackersandslackers.com/multiple-versions-python-ubuntu/
* venvs in docker: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/


## Thanks

This is really only a wrapper around [ocrmypdf](https://github.com/jbarlow83/OCRmyPDF), [img2pdf](https://github.com/josch/img2pdf), scanbd, sane and a bunch of other utilities. They did all the heavy lifting.

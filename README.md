## Summary

This is an adaptation that uses sane-scan-pdf but based on existing files.  The idea being that scanning could be done on a low powered device (i.e. a Raspberry Pi) than the scanned data sent to this docker image for processing.  While if it possible to do all the scanning and processing directly on the Pi it is prohibitively slow, even on a Pi 4.

## Resources

* Managing python versions on ubuntu: https://hackersandslackers.com/multiple-versions-python-ubuntu/
* venvs in docker: https://pythonspeed.com/articles/activate-virtualenv-dockerfile/


TODO:
- Make the scanbd script more robust.
- Document the flow
- Code: read paths from os.environ
- readd the delete functionality
- add validation to ensure that all the files in the folder other than the manifest are in the manifest.
- setup rsync in crontab using flock to prevent dupe runs (https://stackoverflow.com/questions/9390134/rsync-cronjob-that-will-only-run-if-rsync-isnt-already-running)
- include scan.sh and crontab examples in this repo.


Flow:

1. sane + scanadf and scanbd on the pi.
2. Scans the raw data and adds a file manifest with `shasum -a 1 scan-*`
3. Leave it in a auto sync directory (in my case a cronjob rsync task)
4. Docker runs on a more powerful computer that periodically scans the sync'ed local folder and when it finds folders that contain a manifest it attempts to create the pdf.

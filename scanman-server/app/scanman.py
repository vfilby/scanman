 #!/usr/bin/env python3
import os
import sys
import time
import queue
import logging
import multiprocessing
import subprocess
import ocrmypdf
import glob
from subprocess import Popen
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from threading import Thread

scan_jobs = multiprocessing.JoinableQueue()

EVENT_TIMEOUT=5
COMPLETED_TRIGGER="._complete"
WATCH_PATH=os.environ['INTAKE_DIR']
COMPLETED_PATH=os.environ['COMPLETED_DIR']
SCAN_PREFIX="scan-"

class FileWatcherEventHandler(FileSystemEventHandler):
    log = logging.getLogger("FileWatcherEventHandler")
    def __init__( self ):
        FileSystemEventHandler.__init__(self)

    @staticmethod
    def on_any_event(event):
        if event.event_type in ["created","deleted"]:
            FileWatcherEventHandler.log.info("Filesystem %s event - % s." % (event.event_type, event.src_path) )
        scan_jobs.put( event )


def configure_logger():
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
        datefmt="%H:%M:%S",
        stream=sys.stdout)

def consume_lines(pipe, consume):
    with pipe:
        for line in iter(pipe.readline, b''): #NOTE: workaround read-ahead bug
            consume(line)

def process_scan( path ):
    log = logging.getLogger()
    log.info( "Processing Scan" )
    base_path = os.path.normpath( WATCH_PATH )
    scan_directory = os.path.normpath( os.path.dirname( path ) )
    scan_pattern = os.path.join( scan_directory, "%s*"%SCAN_PREFIX )

    filename = "%s" % os.path.basename( scan_directory )
    out_path = "%s.pdf"%os.path.join(COMPLETED_PATH, filename)
    no_ocr_path = "%s.no_ocr.pdf"%os.path.join(base_path, filename)


    log.debug( "base_path, scan_directory: (%s, %s)" %(base_path,scan_directory) )

    if( base_path == scan_directory ):
        log.error( "%s found in root watch directory, each scan should be in it's own subdirectory", COMPLETED_TRIGGER )
        return

    stdout_reader = lambda line: log.info( line )
    stderr_reader = lambda line: log.error( line )

    #cmd = ["/scanman/sane-scan-pdf/scan","-dir",scan_directory,"-o",out_path]
    scan_files = sorted( glob.glob(scan_pattern) )
    cmd = ["img2pdf", "-v", "-o", no_ocr_path] + scan_files
    log.info( "cmd: %s" % " ".join( cmd ) )
    try:
        p = Popen( cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        Thread( target=consume_lines, args=[p.stdout, log.debug] ).start()
        Thread( target=consume_lines, args=[p.stderr, log.debug] ).start()
        p.wait()
    except FileNotFoundError as fnfe:
        log.error( fnfe )


    ocrmypdf.ocr( no_ocr_path, out_path, rotate_pages=True, deskew=True, clean=True )



    # popen that thing

def main():
    log = logging.getLogger()
    # queue up any matching directories already present

    # Look for new ones.
    log.info( "Launching watcher for %s" % WATCH_PATH)

    log.debug( "Configuring file system observer" )
    observer = Observer()
    event_handler = FileWatcherEventHandler()
    observer.schedule(event_handler, WATCH_PATH, recursive = True)
    observer.start()
    log.info( "File system watcher started" )

    log.debug( "Waiting for events..." )
    try:
        while True:
            try:
                log.debug( "get() job from queue." )
                event = scan_jobs.get(timeout=EVENT_TIMEOUT)
                if event.is_directory:
                    log.debug( "Skipping directory event" )
                    scan_jobs.task_done()
                    continue

                log.debug( "src_path: %s" % event.src_path )
                log.debug( "event_type: %s" % event.event_type )
                log.debug( "WATCH_PATH: %s" % WATCH_PATH )

                short_path = event.src_path[len(WATCH_PATH):]
                log.debug( "short_path: %s" % short_path )

                if short_path.endswith( COMPLETED_TRIGGER ):
                    log.info( "%s found, processing %s" % (COMPLETED_TRIGGER, event.src_path) )
                    process_scan( event.src_path )

                scan_jobs.task_done()

            except queue.Empty:
                log.debug( "get() timed out, queue empty" )
                pass

    except KeyboardInterrupt:
        log.info( "SIGINT received: stopping observer" )
        observer.stop()

    observer.join()

if __name__ == "__main__":
    configure_logger()
    main()

 #!/usr/bin/env python3
import os
import sys
import time
import logging
import multiprocessing
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

tasks = multiprocessing.JoinableQueue()

class FileWatcher:
    def __init__(self, watch_path ):
        self.observer = Observer()
        self.watchDirectory = watch_path

    def run(self):
        event_handler = FileWatcherEventHandler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = False)
        self.observer.start()
        print( "observer started" )
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class FileWatcherEventHandler(FileSystemEventHandler):


    def __init__( self ):
        FileSystemEventHandler.__init__(self)

    @staticmethod
    def on_any_event(event):
        print("Watchdog received %s event - % s." % (event.event_type, event.src_path) )
        tasks.put( event )


class Worker(multiprocessing.Process):

    def __init__( self, task_queue ):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue

    def run(self):
        print( "Starting worker cycles" )
        proc_name = self.name
        while True:
            print( "get task" )
            next_task = self.task_queue.get()
            if next_task is None:
                # sit tight, have a nap and try again.
                time.sleep(5)
                print( "continuing" )
                continue
            print( next_task )
            self.task_queue.task_done()
        return


if __name__ == "__main__":

    print( "Launching watcher for %s" % os.environ['INTAKE_DIR'])


    watch = FileWatcher( os.environ['INTAKE_DIR'] )

    print( "starting worker" )

    w = Worker( tasks )
    w.start()
    print( "worker started" )

    # blocks until file watcher is stopped.
    print( "starting watcher" )
    watch.run()

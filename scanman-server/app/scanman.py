#!/usr/bin/env python3
import os
import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

class FileWatcher:


    def __init__(self, watch_path ):
        self.observer = Observer()
        self.watchDirectory = watch_path

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.watchDirectory, recursive = True)
        self.observer.start()
        print( "observer started" )
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        print( event.event_type )
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Event is created, you can process it now
            print("Watchdog received created event - % s." % event.src_path)
        elif event.event_type == 'modified':
            # Event is modified, you can process it now
            print("Watchdog received modified event - % s." % event.src_path)





if __name__ == "__main__":
    print( "Launching scanman" )
    watch = FileWatcher( os.environ['INTAKE_DIR'] )
    watch.run()
    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s - %(message)s',
    #                     datefmt='%Y-%m-%d %H:%M:%S')
    # #path = sys.argv[1] if len(sys.argv) > 1 else '.'
    # path = os.environ['INTAKE_DIR']
    # #event_handler = LoggingEventHandler()
    # event_handler = Handler()
    # observer = Observer()
    # observer.schedule(event_handler, path, recursive=False)
    # observer.start()
    # try:
    #     while True:
    #         time.sleep(1)
    # finally:
    #     observer.stop()
    #     observer.join()

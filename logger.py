import threading
import atexit
import time
import traceback
import sys
from io import StringIO


logfile = None
log_queue = []

def startFileLogging():
    global logfile
    filename = time.ctime().replace(" ", "_")
    logfile = open("logs/" + filename + ".txt", "w")
    thread = threading.Thread(target=loggingThread, daemon=True)
    thread.start()

def loggingThread():
    global logfile
    while True:
        if len(log_queue) > 0:
            logfile.write(log_queue[0]+"\n")
            log_queue.pop(0)

def log(string, doPrint=True):
    global logfile
    log_queue.append(time.ctime() + " - " + string)
    if doPrint:
        print(string)

def exit_handler():
    global logfile
    if not logfile is None:
        logfile.close()

atexit.register(exit_handler)
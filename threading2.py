#!/usr/bin/env python

import threading
import time

exitFlag = 0
globalFlag = 20;

class globalSigs(object):
    def __init__(self,counter):
	self.count = counter;

    def _get_global_count_and_decr(self):
	self.count -= 1;
        return self.count

    def _decr_global_count(self):
        self.count -= 1;

def print_time(threadName, globals):
    threadLock.acquire()
    xyz = globals._get_global_count_and_decr()
    threadLock.release()
    while (xyz > 0):
        print "%s: %s" % (threadName, xyz)
	#globals._decr_global_count()
        threadLock.acquire()
        xyz = globals._get_global_count_and_decr()
        threadLock.release()
	time.sleep(.1);
        if exitFlag:
            thread.exit()

class myThread (threading.Thread):
    def __init__(self, threadID, name, globals):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
	self.globals = globals
    def run(self):
        print "Starting " + self.name
        print_time(self.name, self.globals)
        print "Exiting " + self.name

# Create new threads
globals = globalSigs(20);
threadLock = threading.Lock()
thread1 = myThread(1, "Thread-1", globals)
thread2 = myThread(2, "Thread-2", globals)

# Start new Threads
thread1.start()
thread2.start()

print "Exiting Main Thread"

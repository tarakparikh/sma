#!/usr/bin/env python

import threading
import time

exitFlag = 0

class myThreadClass (threading.Thread):
    def __init__(self, threadID, name, client, clientFunc):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
	self.client = client
	self.clientFunc = clientFunc
    def run(self):
        print "Starting " + self.name
        self.clientFunc(self.name)
        print "Exiting " + self.name


def run_threads(numThreads, client, clientFunc):
    threads = []
    client.threadLock = threading.Lock()

    # Create the threads
    for i in range(0,numThreads):
        threadName = "Thread=%s" % (i)
        threadvar = myThreadClass(i,threadName, client, clientFunc)
        threads.append(threadvar)

    # start the threads
    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()



# Use Model
#
#class abcd:
    #def __init__(self):
        #self.name = "ABCD"
    #def called_from_threads(self, threadName):
        #print self.name
#
#myabcd = abcd()
#run_threads(10,myabcd,myabcd.called_from_threads)
#print "Exiting Main Thread"

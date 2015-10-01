# Thread testing playground

# Note that I am not importing into this namespace so that usage is explicit
import threading
import queue
import readline

class ThreadTest(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        mainq = get_main_queue()
        running = True

# Assume we run forever. Who would want to stop?
        while running:
            try:
                job = mainq.get()
            except Exception as e:
                print("main queue get failed:", e)
                job = None

#   If we get a null job (or a queue error) then exit which will terminate the thread
            if job is not None and job.func is not None:
                job.run()
            else:
                print("main queue stopping")
                running = False

class Job:
    def __init__(self, func, args=(), kwargs={}):
        print("Init Job")
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.func(*self.args, **self.kwargs)

_queuedict = dict()

def get_queue(queuename) -> queue.Queue:
    global _queuedict
    print("get_queue", queuename)

    if queuename not in _queuedict:
        print("Create queue", queuename)
        _queuedict[queuename] = queue.Queue()

    return _queuedict[queuename]

def get_main_queue() -> queue.Queue:
    print("get_main_queue")
    return get_queue("main")

def dispatch_main(func, args=(), kwargs={}):
    print("Dispatch main")
    dispatch_queue("main", func, args, kwargs)

def dispatch_queue(queuename, func, args=(), kwargs={}):
    print("Dispatch queue:", queuename)
    act_queue = get_queue(queuename)
    try:
        act_queue.put(Job(func, args, kwargs))
    except:
        print("Put to", queuename, "queue failed.")

if __name__ == "__main__":
    print("Running in __main__")
    def testit(msg):
        print("Testit dispatched:", msg)

    dispatch_main(testit, args=("Your message here ...",))

    main = ThreadTest()
    main.start()
    try:
        s = input("Msg? ")
        while len(s) > 0:
            dispatch_main(testit, args=(s,))
            s = input("Msg? ")
    except Exception as e:
        print("Oops ... ", e)

# Put the poison pill on the queue
    dispatch_main(None)

    main.join()

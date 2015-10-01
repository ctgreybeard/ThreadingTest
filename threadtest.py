# Thread testing playground

# Note that I am not importing into this namespace so that usage is explicit
import threading

class ThreadTest(threading.Thread):
    pass


if __name__ == "__main__":
    print("Running in __main__")

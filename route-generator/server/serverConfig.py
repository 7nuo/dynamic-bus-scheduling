class Mutex(object):
    def __init__(self):
        self.val = 0

    def incr(self):
        self.val += 1


def changer():
    mutex.incr()

mutex = Mutex()
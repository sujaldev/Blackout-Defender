from threading import Thread, Event


def call_repeatedly(interval, func, *args, **kwargs):
    # https://stackoverflow.com/a/22498708/15007549
    stopped = Event()

    def loop():
        while not stopped.wait(interval):
            func(*args, **kwargs)

    Thread(target=loop).start()
    return stopped.set

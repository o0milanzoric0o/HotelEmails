from datetime import timedelta
from time import time, localtime, strftime


# TIME measuring definitions
def seconds_to_str(t):
    return str(timedelta(seconds=t))


def time_to_str(t):
    return strftime("%H:%M:%S", t)


line = "=" * 40


def log(s, elapsed=None):
    print(line)
    print(time_to_str(localtime()), '-', s)
    if elapsed:
        print("Elapsed time:", elapsed)
    print(line)
    print()


def end_log(start):
    end = time()
    elapsed = end - start
    log("End Program", seconds_to_str(elapsed))


def elapsed_from(start_stamp):
    end = time()
    elapsed = end - start_stamp
    log("Elapsed time: ", seconds_to_str(elapsed))


def now():
    return seconds_to_str(time())

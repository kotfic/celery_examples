from __future__ import absolute_import
from fib import app
import time

@app.task
def fib(n):
    if n < 2:
        return n
    return fib(n - 2) + fib(n - 1)


@app.task
def add(a, b, sleep=0):
    time.sleep(sleep)

    print("Adding {} and {}".format(a, b))

    return a + b


@app.task
def mul(a, b, sleep=0):
    time.sleep(sleep)

    print("Multiplying {} and {}".format(a, b))

    return a * b


@app.task
def xsum(a):
    print("Summing {}".format(a))

    return sum(a)

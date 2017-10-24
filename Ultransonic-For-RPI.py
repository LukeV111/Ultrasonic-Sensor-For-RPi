#!/usr/bin/python3.4

import RPi.GPIO as GPIO
from time import sleep
from time import time
import threading
sleep(30)
from urllib.request import urlopen
content = urlopen("http://www.nowitspersonal.co.za/puristcoffee/index.php?coffeeshop=10&machinenumber=1")

try:
    from Queue import Queue
except:  # python3
    from queue import Queue


GPIO.setmode(GPIO.BOARD) # use board pin numbers - selcted board, not BCM
# define pin #7 as input pin
pin = 7
GPIO.setup(pin, GPIO.IN)
list = ["Start"]


def get_input_task(q):
    while 1:
        if GPIO.input(pin) == GPIO.LOW:  # read input here
            q.put(GPIO.input(pin))  # send it to the queue
            # should not keep reading, just need some interval to next sampling
            sleep(0.3)

input_queue = Queue()
# create a thread to get input
input_th = threading.Thread(target=get_input_task, args=(input_queue,))
input_th.setDaemon(True)
input_th.start()


start = time()

while 1:
    # check the timeout first
    if time() - start > 4:  # 3.5s timeout, list start again
        print ("Timeout, start again")
        list = ["Start"]
        start = time()

    while not input_queue.empty():
        input_queue.get_nowait()  # get the input value
        # no needs to verdict 'val',
        # since we already done in input_read_task
        # it's always LOW
        if len(list) <= 3:
            list.insert(0, "Entry")  # This inserts an item to the list at the first point
            # sleep(0.2)  # already wait in input_read_task, not need sleep here
            print ("Not Done")
            print (len(list))
        elif len(list) > 3:
            list = ["Start"]
            start = time()  # Done, reset the start timestamp
            print ("Done")
            urlopen("http://www.nowitspersonal.co.za/puristcoffee/index.php?coffeeshop=10&machinenumber=1")

            
    sleep(0.1)  # make CPU no so busy, maybe you can consider move
    # 'sleep(0.5)' in line 40 to here

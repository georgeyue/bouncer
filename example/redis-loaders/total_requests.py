#!/usr/bin/python

import socket
import time
import redis
import shared

r = redis.StrictRedis(host='localhost', port=6379, db=0)
b = shared.BatchCounter(5,20000)

metric = {}

def process_data(data):
  global metric
  #print data
  if data['type'] == 'request':
    time = data['time']/1000
    TIME_LENGTH=10

    try:
      metric[time] += 1
    except:
      metric[time] = 1

    if b.check():
      #using slices in these because it seems faster..
      for k,v in metric.items():
        r.incrby(k, v)

      metric.clear()


agg = shared.AggregatorConnector()

while True:
  for d in agg.json_read():
    process_data(d)

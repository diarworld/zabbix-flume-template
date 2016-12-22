#!/usr/bin/python
import argparse
import requests
import json
import sys
import os
import time


class ZabbixFlume():

    def __init__(self):
        self.address = 'localhost'
        self.port = '41414'
        self.tmp_cache_dir = '/tmp'
        self.ret_result = []
        self.final_result_dict = {}

    def collect_metrics(self):
        self.final_result_dict = {}
        self.api_address = 'http://{0}:{1}/metrics'.format(
            self.address, self.port)
        self.ret_result = requests.get(url=self.api_address)
        if len(self.ret_result.text) != 0:
            return self.ret_result.text

    def get_cache(self, ttl=60):
        cache = '{0}/flume-stats.json'.format(self.tmp_cache_dir)
        lock = '{0}/flume-stats.lock'.format(self.tmp_cache_dir)
        jtime = os.path.exists(cache) and os.path.getmtime(cache) or 0
        if time.time() - jtime > ttl and not os.path.exists(lock):
            open(lock, 'a').close()
            try:
                cache_json = self.collect_metrics()
            except:
                cache_json = '{"error":"Unable to get metrics"}'
            with open(cache, 'w') as f:
                f.write(cache_json)
            os.remove(lock)
        ltime = os.path.exists(lock) and os.path.getmtime(lock) or None
        if ltime and time.time() - ltime > ttl * 5:
            os.remove(lock)
        return json.load(open(cache))

    def discovery(self, flows):
        d = {'data': []}
        cache = self.get_cache()
        for k in cache:
            if cache[k]['Type'] == flows.upper():
                d['data'].append({'{#NAME}': k})
        print json.dumps(d)

    def check_metrics(self, flow, metric):
        cache = self.get_cache()
        r = 0
        for k in cache:
            if k == flow:
                if metric in cache[k]:
                    r = cache[k].get(metric)
            elif k == "error":
                r = -1
        return r

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Simple python script for checking flume metrcis via http')
    parser.add_argument('--discover', '-d', metavar=('type'),
                        help='Discover all flume flows by type')
    parser.add_argument('--check', '-c', nargs=2,
                        metavar=('flow', 'metric'), help='Check specified metric')
    parser.add_argument('--address', '-a',
                        help='Flume address. Default is: localhost')
    parser.add_argument('--port', '-p', type=int,
                        help='Flume http port. Default is: 41414')
    args = parser.parse_args()
    zf = ZabbixFlume()
    if args.address is not None:
        zf.address = args.address
    if args.port is not None:
        zf.port = args.port
    if args.discover is not None:
        zf.discovery(args.discover)
    if args.check is not None:
        flow = args.check[0]
        metric = args.check[1]
        print zf.check_metrics(flow, metric)


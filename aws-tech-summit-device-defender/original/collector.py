"""
Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.

  Licensed under the Apache License, Version 2.0 (the "License").
  You may not use this file except in compliance with the License.
  A copy of the License is located at

      http://www.apache.org/licenses/LICENSE-2.0

  or in the "license" file accompanying this file. This file is distributed
  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
  express or implied. See the License for the specific language governing
  permissions and limitations under the License.
 """

import psutil as ps
import socket
from metrics import Metrics
import argparse
from time import sleep


class Collector(object):
    """Collector

    Reads system information and populates a metrics object.
    This implementation utilizes psutil to make parsing metrics easiser and more cross-platform.
    """

    def __init__(self, thing_name, short_metrics_names=False):
        """Initialize the collector

        Parameters
        ----------
        thing_name : str
                Thing Name as assigned to this device in AWS Iot Device Management
        short_metrics_names : bool
                Toggle short object tags in output metrics.
        """
        self._thing_name = thing_name

        # Keep a copy of the last metric, if there is one, so we can calculate change in some metrics.
        self._last_metric = None
        self._short_names = short_metrics_names

    def listening_ports(self, metrics):
        for conn in ps.net_connections(kind='inet'):
            if conn.status == "LISTEN" and conn.type == socket.SOCK_STREAM:
                metrics.listening_tcp_ports.append(conn.laddr.port)
            if conn.type == socket.SOCK_DGRAM:  # on Linux, udp socket status is always "NONE"
                metrics.listening_udp_ports.append(conn.laddr.port)

    def network_stats(self, metrics):
        net_counters = ps.net_io_counters(pernic=False)
        metrics.add_network_stats(
            net_counters.bytes_recv,
            net_counters.bytes_sent,
            net_counters.packets_recv,
            net_counters.packets_sent)

    def network_connections(self, metrics):
        protocols = ['tcp']
        for protocol in protocols:
            for c in ps.net_connections(kind=protocol):
                try:
                    if c.status == "ESTABLISHED" or c.status == "BOUND":
                        metrics.add_network_connection(c.raddr.ip, c.raddr.port)
                except Exception as ex:
                    print ('Failed to parse network info for protocol: ' + protocol)
                    print (ex)

    def collect_metrics(self):
        """Sample system metrics and populate a metrics object suitable for publishing to Device Defender"""
        metrics_current = Metrics(client_id=self._thing_name,
                                  short_names=self._short_names, last_metric=self._last_metric)

        self.network_stats(metrics_current)
        self.listening_ports(metrics_current)
        self.network_connections(metrics_current)

        self._last_metric = metrics_current
        return metrics_current


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sample_rate", action="store", dest="sample_rate", required=False,
                        help="Interval between individual samples, cannot exceed Upload Rate")
    parser.add_argument("-n", "--number_samples", action="store", dest="number_samples", default=0, required=False,
                        help="Number of samples to collect before exiting")
    parser.add_argument("-l", "--list_size", action="store",
                        dest="max_list_size", default=None, required=False)
    parser.add_argument("--short-names", action="store_true", dest="short_names", default=False, required=False,
                        help="Produce Metric Report with Short Names")

    args = parser.parse_args()
    collector = Collector("THING_NAME", short_metrics_names=args.short_names)

    if args.sample_rate:
        count = int(args.number_samples)
        while True:
            count -= 1
            # setup a loop to collect
            metric = collector.collect_metrics()
            print (metric.to_json_string(pretty_print=True))

            if count == 0:
                break

            sleep(float(args.sample_rate))

    else:
        metric = collector.collect_metrics()

        if args.max_list_size:
            metric.max_list_size = int(args.max_list_size)

        print (metric.to_json_string(pretty_print=True))
        exit()

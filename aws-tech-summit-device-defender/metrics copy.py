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

import time
import json
import cbor
import random
import os
from tags import Tags


class Metrics(object):
    """Metrics

    A collection of system metric values, providing facilities for output in a Device Defender compliant format.


    Features:
        Metrics can be exported in either cbor or JSON format.
        Delta metrics: if the class is initialized with a existing metrics object,
           for certain metrics, the difference between the old an current metric value will calculated and stored.
        Selectable metric tags, allow for verbose metrics tags, for easier debugging, or short memonic tags,
        reducing the amount data transmitted and stored in memory.


    """

    def __init__(self, client_id, short_names=False, last_metric=None):
        """Initialize a new metrics object

        Parameters
        ----------
        client_id : str
                Unique identifier for the device that emitted the metrics
        short_names : bool
                Toggle short object tags in output metrics.
        last_metric : Metrics object
                Metric object used for delta metric calculation.
        """
        self.t = Tags(short_names)
        # Header Information
        self.client_id = client_id
        self._timestamp = int(time.time())
        if last_metric is None:
            self.interval = 0
        else:
            self.interval = self._timestamp - last_metric._timestamp

        # Network Metrics
        self._net_connections = []
        self.listening_tcp_ports = []
        self.listening_udp_ports = []
        
        # PCR Metrics
        self.pcr_measurement = []

        # Network Stats By Interface
        self._interface_stats = {}
        if last_metric is None:
            self._old_interface_stats = {}
        else:
            self._old_interface_stats = last_metric._interface_stats

        self.max_list_size = 50

    @property
    def network_stats(self):
        """Retrieve network stats, per interface"""
        return self._interface_stats

    def add_network_stats(self, bytes_in, packets_in, bytes_out, packets_out):
        """
        Add cumulative network stats across all network interfaces.
        If the a previous metrics object was supplied,attempts to calculate and store delta metric

        Parameters
        ----------
        bytes_in: int
           Number of bytes received on this interface
        bytes_out: int
           Number of bytes sent from this interface
        packets_in: int
           Number of packets received on this interface
        packets_out: int
           Number of packets sent from this interface
        """
        if self._old_interface_stats:
            bytes_in_diff = bytes_in - self._old_interface_stats[self.t.bytes_in]
            bytes_out_diff = bytes_out - self._old_interface_stats[self.t.bytes_out]
            packets_in_diff = packets_in - self._old_interface_stats[self.t.packets_in]
            packets_out_diff = packets_out - self._old_interface_stats[self.t.packets_out]

            self._interface_stats = {self.t.bytes_in: bytes_in_diff,
                                     self.t.bytes_out: bytes_out_diff,
                                     self.t.packets_in: packets_in_diff,
                                     self.t.packets_out: packets_out_diff}

        else:
            self._interface_stats = {self.t.bytes_in: bytes_in, self.t.bytes_out: bytes_out,
                                     self.t.packets_in: packets_in,
                                     self.t.packets_out: packets_out}

    def add_network_connection(self, remote_addr, remote_port):
        """ Add network connection details

        Parameters
        ----------
        remote_addr: string
            Ip address of the remote peer, can be ipv4 or ipv6
        remote_port: integer
            Port of the remote peer
        """
        self._net_connections.append({self.t.remote_addr: remote_addr + ":" + str(remote_port)})

    @property
    def network_connections(self):
        return self._net_connections

    def _sample_list(self, input_list):
        if self.max_list_size and len(input_list) > self.max_list_size:
            random.seed(os.urandom(50))
            output_list = random.sample(input_list, self.max_list_size)
            return output_list
        else:
            return input_list

    def to_json_string(self, pretty_print=False):
        """Convert the metrics to a json string suitable for DeviceDefender

        Parameters
        ----------
        pretty_print: bool
            Set to true if you would like json to be formatted in a more human-friendly format

        """
        metrics = self._v1_metrics()
        if pretty_print:
            return json.dumps(metrics, indent=4, sort_keys=True)
        else:
            return json.dumps(metrics, separators=(',', ':'))

    def to_cbor(self):
        """Returns a cbor serialized metrics object """
        return cbor.dumps(self._v1_metrics())

    def _v1_metrics(self):
        """Format metrics in Device Defender version 1 format"""
        t = self.t
        header = {t.report_id: self._timestamp,
                  t.version: "1.0"}
        metrics = {}

        if self.network_stats:
            metrics[t.interface_stats] = self.network_stats

        if self._net_connections:
            metrics[t.tcp_conn] = {t.connections: self._sample_list(self._net_connections),
                                   t.total: len(self._net_connections)}
        if self.listening_tcp_ports:
            metrics[t.listening_tcp_ports] = {t.ports: self._sample_list(self.listening_tcp_ports),
                                              t.total: len(self.listening_tcp_ports)}
        if self.listening_udp_ports:
            metrics[t.listening_udp_ports] = {t.ports: self._sample_list(self.listening_udp_ports),
                                              t.total: len(self.listening_udp_ports)}
        report = {t.header: header,
                  t.metrics: metrics}

        return report

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

# KG - Adding constants to control location of files and index of PCRs
BASE_MEASUREMENT_DIR = "/home/pi/arc_kg_demo_082018/aws-tech-summit-tpm/"
RUNTIME_MEASURE_FILE = BASE_MEASUREMENT_DIR + "demoapp/data/runtime_measurements"
RUNTIME_PCR_FILE = BASE_MEASUREMENT_DIR + "demoapp/data/runtime_pcr"
RUNTIME_PCR_INDEX = 10

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

    
    # KG - Adding PCR measurement to the metrics
    def pcr_measurement(self, metrics):
        #print ("adding pcr measurement")
        #KG - Runtime measurement in IMA format
        ima = open(RUNTIME_MEASURE_FILE,'r')
        #KG - Runtime measurements obtained from PCR
        tpm = open(RUNTIME_PCR_FILE,'r')
        pcr_ima_dictionary = {}
        pcr_tpm_dictionary = {}
        violation = "" 
       
        measured_values_dictionary = {}

        i=0
        for line in ima:
            #print (line)
            lineTokens = line.split()
            pcr_ima_dictionary ["pcr"+str(RUNTIME_PCR_INDEX)] = lineTokens[1]
            i=i+1
        
        i=0
        for line in tpm:
            #print (line)
            lineTokens = line.split()
            pcr_tpm_dictionary ["pcr"+str(i)] = lineTokens[1]
            i=i+1
        
        measured_values_dictionary ["kernel_measured_value"] =  pcr_ima_dictionary 
        measured_values_dictionary ["pcr_runtime_value"] =  pcr_tpm_dictionary
        measured_values_dictionary ["device_integrity"] = "NO_VIOLATION"
        
        if (len(pcr_tpm_dictionary) <RUNTIME_PCR_INDEX):
            print "The size of PCR is less than expected. Throwing a violation!!"
            measured_values_dictionary ["device_integrity"] = "VIOLATION"
        elif (pcr_ima_dictionary["pcr"+str(RUNTIME_PCR_INDEX)] != pcr_tpm_dictionary["pcr"+str(RUNTIME_PCR_INDEX)]):
            measured_values_dictionary ["device_integrity"] = "VIOLATION"
                 
        metrics.add_pcr_measurement(measured_values_dictionary)
                  
    def collect_metrics(self):
        """Sample system metrics and populate a metrics object suitable for publishing to Device Defender"""
        metrics_current = Metrics(client_id=self._thing_name,
                                  short_names=self._short_names, last_metric=self._last_metric)

        self.network_stats(metrics_current)
        self.listening_ports(metrics_current)
        self.network_connections(metrics_current)
        # KG - Adding PCR measurement to the metrics
        self.pcr_measurement (metrics_current)
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
            # print (metric.to_json_string(pretty_print=True))

            if count == 0:
                break

            sleep(float(args.sample_rate))

    else:
        metric = collector.collect_metrics()

        if args.max_list_size:
            metric.max_list_size = int(args.max_list_size)

        # print (metric.to_json_string(pretty_print=True))
        exit()

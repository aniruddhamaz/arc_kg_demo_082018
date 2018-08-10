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

import pytest
from AWSIoTDeviceDefenderAgentSDK import metrics, tags


@pytest.fixture
def simple_metric():
    m = metrics.Metrics(client_id="FAKE_CLIENT_ID")

    m.add_network_stats(bytes_in=100, packets_in=50, bytes_out=200, packets_out=150)
    m.add_network_connection("10.10.10.10", 80)
    m.add_network_connection("11.11.11.11", 80)

    m.listening_tcp_ports += [80, 88, 8000, 43]
    m.listening_udp_ports += [999, 980, 9032]
    return m


@pytest.fixture
def simple_metric_short_names():
    m = metrics.Metrics(short_names=True, client_id="FAKE_CLIENT_ID")

    m.add_network_stats(bytes_in=100, packets_in=50, bytes_out=200, packets_out=150)
    m.add_network_connection("10.10.10.10", 80)
    m.add_network_connection("11.11.11.11", 80)

    m.listening_tcp_ports += [80, 88, 8000, 43]
    m.listening_udp_ports += [999, 980, 9032]
    return m


def test_v1_metrics_basic_structure_long_names(simple_metric):
    t = metrics.Tags()
    report = simple_metric._v1_metrics()

    # overall structure
    assert t.header in report
    assert t.metrics in report

    # header elements
    header_block = report[t.header]
    assert t.report_id in header_block
    assert t.version in header_block

    metric_block = report[t.metrics]
    # top-level element in metrics block
    assert t.interface_stats in metric_block
    assert t.listening_tcp_ports in metric_block
    assert t.listening_udp_ports in metric_block
    assert t.tcp_conn in metric_block


def test_v1_metrics_basic_structure_short_names(simple_metric_short_names):
    t = metrics.Tags(short_names=True)
    report = simple_metric_short_names._v1_metrics()

    # Overall Structure
    assert t.header in report
    assert t.metrics in report

    # header elements
    header_block = report[t.header]
    assert t.report_id in header_block
    assert t.version in header_block

    metric_block = report[t.metrics]
    # top-level element in metrics block
    assert t.interface_stats in metric_block
    assert t.listening_tcp_ports in metric_block
    assert t.listening_udp_ports in metric_block
    assert t.tcp_conn in metric_block


def test_v1_metrics_optional_elements(simple_metric):
    t = metrics.Tags(short_names=False)
    report = simple_metric._v1_metrics()

    metric_block = report[t.metrics]
    # top-level element in metrics block
    assert t.interface_stats in metric_block
    assert t.listening_tcp_ports in metric_block
    assert t.listening_udp_ports in metric_block
    assert t.tcp_conn in metric_block

    assert t.listening_udp_ports in report[t.metrics]

    simple_metric._interface_stats = {}
    simple_metric.listening_tcp_ports = []
    simple_metric.listening_udp_ports = []
    simple_metric._net_connections = []

    report = simple_metric._v1_metrics()
    metric_block = report[t.metrics]

    assert t.interface_stats not in metric_block
    assert t.listening_tcp_ports not in metric_block
    assert t.listening_udp_ports not in metric_block
    assert t.tcp_conn not in metric_block


def test_v1_sampled_lists(simple_metric):
    simple_metric.max_list_size = 10
    t = metrics.Tags()

    for i in range(1, 20):
        simple_metric.add_network_stats(1, 1, 1, 1)
        simple_metric.add_network_connection("a", "1")
        simple_metric.add_network_connection("a", "1")
        simple_metric.listening_tcp_ports.append(i)
        simple_metric.listening_udp_ports.append(i)

    report = simple_metric._v1_metrics()
    metric_block = report[t.metrics]

    assert len(metric_block[t.tcp_conn][t.connections]) == 10
    assert metric_block[t.tcp_conn][t.total] > len(
        metric_block[t.tcp_conn][t.connections])
    assert len(metric_block[t.listening_tcp_ports][t.ports]) == 10
    assert metric_block[t.listening_tcp_ports][t.total] > len(
        metric_block[t.listening_tcp_ports][t.ports])
    assert len(metric_block[t.listening_udp_ports][t.ports]) == 10
    assert metric_block[t.listening_udp_ports][t.total] > len(
        metric_block[t.listening_udp_ports][t.ports])


def test_listening_ports(simple_metric):
    assert len(simple_metric.listening_tcp_ports) == 4
    assert len(simple_metric.listening_udp_ports) == 3
    assert 80 in simple_metric.listening_tcp_ports
    assert 980 in simple_metric.listening_udp_ports


def test_basic_add_network_stats(simple_metric):
    assert len(simple_metric.network_stats) == 4
    assert simple_metric.network_stats['bytes_in'] == 100
    assert simple_metric.network_stats['packets_in'] == 50
    assert simple_metric.network_stats['bytes_out'] == 200
    assert simple_metric.network_stats['packets_out'] == 150


def test_timestamp(simple_metric):
    m1 = metrics.Metrics("FAKE_CLIENT_ID")
    assert m1._timestamp >= simple_metric._timestamp


def test_network_stats_delta_calculation(simple_metric):
    m1 = metrics.Metrics("FAKE_CLIENT_ID")
    m1.timestamp = 0
    m1.add_network_stats(bytes_in=100, packets_in=50,
                         bytes_out=200, packets_out=150)

    m2 = metrics.Metrics("FAKE_CLIENT_ID", last_metric=m1)
    m2.timestamp = 10
    m2.interval = 10
    m2.add_network_stats(bytes_in=125, packets_in=75,
                         bytes_out=225, packets_out=175)

    assert m2.network_stats['bytes_in'] == 25
    assert m2.network_stats['packets_in'] == 25
    assert m2.network_stats['bytes_out'] == 25
    assert m2.network_stats['packets_out'] == 25


def test_add_network_connections(simple_metric):
    assert len(simple_metric._net_connections) == 2
    assert simple_metric._net_connections[0]['remote_addr'] == '10.10.10.10:80'


def test_field_sizes():
    m = metrics.Metrics("FAKE_CLIENT_ID")

    m.add_network_stats(100, 50, 200, 150)
    m.add_network_connection("10.10.10.10", 80)
    m.listening_tcp_ports += [80, 88, 8000, 43]
    m.listening_udp_ports += [999, 980, 9032]

    assert len(m._net_connections) == 1
    assert len(m.listening_tcp_ports) == 4
    assert len(m.listening_udp_ports) == 3
    assert len(m.network_stats) == 4
    assert m.client_id == "FAKE_CLIENT_ID"


def test_tags():
    t_l = metrics.Tags(False)
    t_s = metrics.Tags(True)


def test_sampled_lists(simple_metric):
    t = metrics.Tags()
    m = metrics.Metrics(client_id="FAKE_CLIENT_ID")
    m.max_list_size = 10

    for i in range(1, 20):
        m.add_network_connection("10.10.10.10", i)
        m.listening_udp_ports.append(i)
        m.listening_tcp_ports.append(i)

    report = m._v1_metrics()
    metric_block = report[t.metrics]
    assert len(metric_block[t.listening_tcp_ports][t.ports]) == 10
    assert len(metric_block[t.listening_udp_ports][t.ports]) == 10
    assert len(metric_block[t.tcp_conn][t.connections]) == 10

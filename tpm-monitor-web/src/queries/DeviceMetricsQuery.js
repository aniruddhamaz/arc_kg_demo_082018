import gql from 'graphql-tag';

export default gql`
query {
  getDeviceMetrics(thing_name: "MyRaspberryPi") {
    thing_name
    id
    device_integrity
    listening_tcp_ports
    listening_udp_ports
    tcp_connections
    measurement {
      kernel_measured_value
      pcr_runtime_value
      pcrIndex
    }
  }
}
`;

import React, { Component } from 'react';
import { css } from 'react-emotion';
import { graphql, compose, withApollo } from "react-apollo";

import { ClipLoader } from 'react-spinners';

import DeviceMetricsQuery from '../queries/DeviceMetricsQuery'

const override = css`
    display: block;
    margin: 0 auto;
    border-color: red;
`;
 
class DeviceMetrics extends Component {

    static defaultProps = {
        deviceMetrics: {},
        data: {},
        interval: {},
        loading: true
    }

    componentDidMount() {
        this.interval = setInterval(() => {
            this.setState( () => {
                console.log("Refreshing........"); 
                this.props.data.refetch();
                //return { time: Date.now() }
            });
        }, 30000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {

        const { deviceMetrics } = this.props;

        console.log("========== Rendering ......");

        return (
            <div>
                <div>
                    <table border="1">
                        <tbody>
                            <tr>
                                <td>Thing Name</td>
                                <td>{deviceMetrics.thing_name}</td>
                                <td>ID</td>
                                <td>{deviceMetrics.id}</td>
                                <td>Device Integrity</td>
                                <td>{deviceMetrics.device_integrity}</td>
                            </tr>
                            <tr>
                                <td>Listening Ports(TCP)</td>
                                <td>{deviceMetrics.listening_tcp_ports}</td>
                                <td>Listening Ports(UDP)</td>
                                <td>{deviceMetrics.listening_udp_ports}</td>
                                <td>TCP Connections</td>
                                <td>{deviceMetrics.tcp_connections}</td>
                            </tr>
                            <tr>
                                <td>PCR # {deviceMetrics.measurement.pcrIndex} Boot Value (TPM)</td>
                                <td>{deviceMetrics.measurement.pcr_runtime_value}</td>
                            </tr>
                            <tr>
                                <td>PCR # {deviceMetrics.measurement.pcrIndex} Runtime Value</td>
                                <td>{deviceMetrics.measurement.kernel_measured_value}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        );

    }
}

export default withApollo(compose(
    graphql(
        DeviceMetricsQuery, 
        {
            options: {
                fetchPolicy: 'network-only'
            },
            props: props => ({
                deviceMetrics: props.data.getDeviceMetrics,
                data: props.data
            })
        }
    )
  )(DeviceMetrics));


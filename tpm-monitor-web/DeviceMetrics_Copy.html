import React, { Component } from 'react';
import { css } from 'react-emotion';
import { graphql, compose, withApollo } from "react-apollo";
import { Link } from 'react-router-dom';
import 'semantic-ui-css/semantic.min.css';

import { ClipLoader } from 'react-spinners';

import DeviceMetricsQuery from '../queries/DeviceMetricsQuery';
import redCircle from '../images/red-circle.png';
import greenCircle from '../images/green-circle.png';

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
        loading: {}
    }

    componentDidMount() {
        this.interval = setInterval(() => {
            this.setState( () => {
                console.log("Refreshing........"); 
                this.loading = true;
                this.props.data.refetch();
            });
        }, 15000);
    }

    componentWillUnmount() {
        clearInterval(this.interval);
    }

    render() {

        const { deviceMetrics } = this.props;

        console.log("========== Rendering ......");

        return (
            <div>
                <br/>
                <div className={`ui container`}>
                    <Link to="/" className="ui button">Back to Thing Registry</Link>
                </div>
                <div className={`ui container raised very padded segment`}>
                    <div className={`ui clearing basic segment`}>
                        <h1 className="ui header center floated">Metrics for {deviceMetrics.thing_name}</h1>
                    </div>

                    <div className="ui cards">
                        <div className="card">
                            <div className="content">
                                <div className="header">
                                    <i className="large blue microchip icon"></i>
                                    Device Status
                                </div>
                            </div>
                            <div className="extra content">
                                <div className="center aligned author">
                                {deviceMetrics.device_integrity == 'VIOLATION'
                                            ? <i className="massive red frown outline icon"></i>
                                            : <i className="massive green smile icon"></i>
                                }
                            </div>
                        </div>                            
                    {/* </div>

                    <div className="ui cards"> */}
                        <div className="card">
                            <div className="content">
                                <div className="header">
                                    <i className="large blue wifi icon"></i>
                                    Network Status
                                </div>
                            </div>
                            <div className="extra content">
                                <div className="ui statistics">
                                    <div class="statistic">
                                        <div className="value">
                                        {deviceMetrics.listening_tcp_ports}
                                        </div>
                                        <div className="label">
                                        TCP Ports
                                        </div>
                                    </div>
                                    <div class="statistic">
                                        <div className="value">
                                        {deviceMetrics.listening_udp_ports}
                                        </div>
                                        <div className="label">
                                        UDP Ports
                                        </div>
                                    </div>
                                    <div class="statistic">
                                        <div className="value">
                                        {deviceMetrics.tcp_connections}
                                        </div>
                                        <div className="label">
                                        TCP Connections
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>                            
                    </div>

                    <div className="ui cards">
                        <div className="card">
                            <div className="content">
                                <div className="header">
                                    <i className="large blue wifi icon"></i>
                                    PCR # {deviceMetrics.measurement.pcrIndex} Data
                                </div>
                            </div>
                            <div className="content">
                                <div className="ui horizontal statistics">
                                    <div class="ui tiny statistic">
                                        <div className="value">
                                        {deviceMetrics.measurement.pcr_runtime_value}
                                        </div>
                                        <div className="label">
                                        Boot Value
                                        </div>
                                    </div>
                                    <div class="ui tiny statistic">
                                        <div className="value">
                                        {deviceMetrics.measurement.kernel_measured_value}
                                        </div>
                                        <div className="label">
                                        Kernel Value
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>                            
                    </div>                    
                </div>
           </div>
        </div>
        );

    }
}

export default withApollo(compose(
    graphql(
        DeviceMetricsQuery, 
        {
            options: ({ match: {params: {thingid}}}) => ({
                fetchPolicy: 'network-only',
                variables: { thingid }
            }),
            props: props => ({
                deviceMetrics: props.data.getDeviceMetrics,
                data: props.data,
                loading: false
            })
        }
    )
  )(DeviceMetrics));


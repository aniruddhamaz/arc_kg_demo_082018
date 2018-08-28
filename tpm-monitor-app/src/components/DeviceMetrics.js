import React, { Component } from 'react';
import { css } from 'react-emotion';
import { graphql, compose, withApollo } from "react-apollo";
import { Link } from 'react-router-dom';
import 'semantic-ui-css/semantic.min.css';
import techSummitLogo from '../TechSummitMacau_white_Logo.png';
import awsIotLogo from '../aws-iot-logo.png';

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


<div className="ui segment">
    <img class="ui centered small image" src={awsIotLogo} />
</div>

<h2 className="ui header center aligned">AWS IoT Device Defender Demo - Chip to Cloud Security</h2>

            
 				<h4 class="ui horizontal divider header">
  <i class="tag icon"></i>
  Device Defender Summary </h4>           
            
				<div class="ui four column grid">
				
				  <div class="column">
				    <div class="ui fluid card">
                            <div className="content">
                                <div className="header">
                                    <i className="large blue microchip icon"></i>
                                    Device Status
                                </div>
                            </div>
                            <div className="extra content ui large statistic">
                                <div className="center aligned author">
                                {deviceMetrics.device_integrity == 'VIOLATION'
                                            ? <i className="massive red frown outline icon"></i>
                                            : <i className="massive green smile icon"></i>
                                }
                                </div>
                            </div>
   					 </div>
  				</div>
				
				  <div class="column">
				    <div class="ui fluid card">
                            <div className="content">
                                <div className="header">
                                    <i className="large blue wifi icon"></i>
                                    Network Status
                                </div>
                            </div>
                                    <div class="extra content ui huge statistic">
                                        <div className="value">
                                        {deviceMetrics.listening_tcp_ports}
                                        </div>
                                        <div className="label">
                                        TCP Ports
                                        </div>
                                    </div> 
   					 </div>
  				</div>
				
				  <div class="column">
				    <div class="ui fluid card">
                            <div className="content">
                                <div className="header">
                                    <i className="large blue wifi icon"></i>
                                    Network Status
                                </div>
                            </div>
                                    <div class="extra content ui huge statistic">
                                        <div className="value">
                                        {deviceMetrics.listening_udp_ports}
                                        </div>
                                        <div className="label">
                                        UDP Ports
                                        </div>
                                    </div> 
   					 </div>
  				</div>
				
				  <div class="column">
				    <div class="ui fluid card">
                            <div className="content">
                                <div className="header">
                                    <i className="large blue wifi icon"></i>
                                    Network Status
                                </div>
                            </div>
                                    <div class="extra content ui huge statistic">
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
				
				<h4 class="ui horizontal divider header">
                    <i class="tag icon"></i>
                    TPM & Kernel Measurement Details 
                </h4>		


                <div className="ui fluid card">
                    <div className="content">
                        <table className="ui orange table">
                            <thead>
                                <tr>
                                    <th>PCR #</th>
                                    <th>Measurement Type</th>
                                    <th>Value</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>{deviceMetrics.measurement.pcrIndex}</td>
                                    <td>Boot</td>
                                    <td>{deviceMetrics.measurement.pcr_runtime_value}</td>
                                </tr>
                                <tr>
                                    <td>{deviceMetrics.measurement.pcrIndex}</td>
                                    <td>Runtime</td>
                                    <td>{deviceMetrics.measurement.kernel_measured_value}</td>
                                </tr>
                            </tbody>
                        </table>
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


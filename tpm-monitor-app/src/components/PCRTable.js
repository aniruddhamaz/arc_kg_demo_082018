import React, { Component } from 'react';
import { Link } from "react-router-dom";
import { graphql, compose, withApollo } from "react-apollo";

import PCRQuery from '../queries/PCRQuery'
import PCRDataSubscription from '../subscriptions/PCRDataSubscription'

class PCRTable extends Component {

    state = {
        busy: false
    }

    static defaultProps = {
        pcrs: [],
    }

    // componentDidMount() {
    //     this.pcrSubscription = this.props.subscribeToPCRUpdates();
    // }

    // componentWillUnmount() {
    //     this.pcrSubscription();
    // }

    // handlePCRDataLoad = async() => {
    //     const { client } = this.props;

    //     console.log("-----------Hello");
    //     const query = PCRQuery;

    //     this.setState({ busy: true });

    //     await client.query({
    //         query,
    //         fetchPolicy: 'network-only'
    //     });

    //     this.setState({ busy: false });
    // }

    renderPCRItem = (item) => (
        <tr key={item.pcrindex}>
            <td>{item.pcrindex}</td>
            <td>{item.bootvalue}</td>
            <td>{item.runtimevalue}</td>
            <td>{item.status}</td>
        </tr>

    );

    render() {

        const { busy } = this.state;
        const { pcrs } = this.props;

        return (
            <div>
                <div>
                    {/* <button className="ui icon left basic button" onClick={this.handlePCRDataLoad} disabled={busy}>
                        <i aria-hidden="true" className={`refresh icon ${busy && "loading"}`}></i>
                        Sync with Server
                    </button> */}
                </div>
                <div>
                    <table border="1">
                        <thead>
                            <tr>
                                <th>PCR #</th>
                                <th>Boot Value</th>
                                <th>Runtime Value</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                        {pcrs.map((pcr) =>
                            this.renderPCRItem(pcr) 
                        )}
                        </tbody>
                    </table>
                </div>
            </div>
        );

    }
}

export default withApollo(compose(
    graphql(
        PCRQuery, 
        {
            options: {
                fetchPolicy: 'network-only'
            },
            props: props => ({
                pcrs: props.data.listPCRsFor,
                // subscribeToPCRUpdates: () => 
                //     props.data.subscribeToMore({
                //         document: PCRDataSubscription,
                //         variables: {
                //             thingid: props.ownProps.thingid
                //         },
                //         updateQuery:(previous, {subscriptionData}) => {
                //             console.log(subscriptionData);
                //             return subscriptionData;
                //         }
                //     })
            })
        }
    )
  )(PCRTable));


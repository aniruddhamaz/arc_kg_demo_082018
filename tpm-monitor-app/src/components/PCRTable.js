import React, { Component } from 'react';
import { graphql, compose, withApollo } from "react-apollo";

import PCRQuery from '../queries/PCRQuery'

class PCRTable extends Component {

    static defaultProps = {
        pcrs: [],
    }

    renderPCRItem = (item) => (
        <tr key={item.thing_name + item.pcr_index}>
            <td>{item.thing_name}</td>
            <td>{item.pcr_index}</td>
            <td>{item.pcr_value}</td>
        </tr>

    );

    render() {

        const { pcrs } = this.props;

        return (
            <div>
                <table border="1">
                    <thead>
                        <tr>
                            <th>Thing Name</th>
                            <th>PCR Index</th>
                            <th>PCR Value</th>
                        </tr>
                    </thead>
                    <tbody>
                    {pcrs.map((pcr) =>
                        this.renderPCRItem(pcr) 
                    )}
                    </tbody>
                </table>
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


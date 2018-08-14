import React, { Component } from 'react';
import { graphql, compose, withApollo } from "react-apollo";

import ListAllThingsQuery from '../queries/ListAllThingsQuery'

class ThingsMaster extends Component {

    static defaultProps = {
        things: [],
    }

    renderThingItem = (item) => (
        <tr key={item.thing_name}>
            <td>{item.thing_name}</td>
            <td>{item.thing_arn}</td>
        </tr>
        
    );

    render() {

        const { things } = this.props;

        return (
            <div>
                <div>
                    <table border="1">
                        <thead>
                            <tr>
                                <th>Thing Name</th>
                                <th>Thing ARN</th>
                            </tr>
                        </thead>
                        <tbody>
                        {things.map((thing) =>
                            this.renderThingItem(thing) 
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
        ListAllThingsQuery, 
        {
            options: {
                fetchPolicy: 'network-only'
            },
            props: props => ({
                things: props.data.listThings,
            })
        }
    )
  )(ThingsMaster));


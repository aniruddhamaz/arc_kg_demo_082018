import React, { Component } from 'react';
import { graphql, compose, withApollo } from "react-apollo";
import { Link } from 'react-router-dom';
import 'semantic-ui-css/semantic.min.css';

import ListAllThingsQuery from '../queries/ListAllThingsQuery'

class ThingsMaster extends Component {

    static defaultProps = {
        things: [],
    }

    renderThing = (thing) => (

        <Link to={`/thing/metrics/${thing.thing_name}`} className="card green" key={thing.thing_name}>
            <div className="content">
                <div className="header">{thing.thing_name}</div>
            </div>
        </Link>

    );

    render() {

        const { things } = this.props;

        return (
            <div>
                <div className={`ui clearing basic segment`}>
                    <h1 className="ui header left floated">Registered Things</h1>
                </div>
                <div className="ui link cards">
                    {things.map((thing) =>
                            this.renderThing(thing) 
                    )}
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


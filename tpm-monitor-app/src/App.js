import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import logo from './logo.svg';
import './App.css';

import { ApolloProvider, graphql, compose } from 'react-apollo';
import AWSAppSyncClient from 'aws-appsync';
import { Rehydrated } from 'aws-appsync-react';
import { AUTH_TYPE } from 'aws-appsync/lib/link/auth-link';
import { Auth } from 'aws-amplify'
import * as AWS from 'aws-sdk';

import AppSync from './AppSync';
import PCRTable from './components/PCRTable';


export class Home extends Component {
  render() {
    return (
      <div className="App">
        <header className="App-header">
          <img src={logo} className="App-logo" alt="logo" />
          <h1 className="App-title">Welcome to React</h1>
        </header>
        <p className="App-intro">
          To get started, edit <code>src/App.js</code> and save to reload.
        </p>
        <PCRTable />
      </div>
    );
  }
}

const App = () => (
  <Router>
    <div>
      <Route exact={true} path="/" component={Home} />
    </div>
  </Router>
);

const client = new AWSAppSyncClient({
  url: AppSync.graphqlEndpoint,
  region: AppSync.region,
  auth: {
      type: AUTH_TYPE.API_KEY,
      apiKey: AppSync.apiKey,

      // type: AUTH_TYPE.AWS_IAM,
      // Note - Testing purposes only
      /*
      credentials: new AWS.Credentials({
          accessKeyId: "AWS_ACCESS_KEY_ID",
          secretAccessKey: "AWS_SECRET_ACCESS_KEY"
      })
      */

      // Amazon Cognito Federated Identities using AWS Amplify
      credentials: () => Auth.currentCredentials(),

      // Amazon Cognito user pools using AWS Amplify
      // type: AUTH_TYPE.AMAZON_COGNITO_USER_POOLS,
      // jwtToken: async () => (await Auth.currentSession()).getIdToken().getJwtToken(),
  },
});


const WithProvider = () => (
  <ApolloProvider client={client}>
      <Rehydrated>
          <App />
      </Rehydrated>
  </ApolloProvider>
);

export default WithProvider;


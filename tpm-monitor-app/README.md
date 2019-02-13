# AWS Setup

## Console URL : 

https://kg-amazon.signin.aws.amazon.com/console


## Making the code work

1. Get the latest code from https://github.com/aniruddhamaz/arc_kg_demo_082018.git
2. Install all required Node modules by running *'npm install'*
3. Install Node modules peer dependencies *'npm install —save apollo-client'*
4. Run using *'npm start'*



## Issues faced

1. [Friday, February 8] Current code status is not correct. The schema definition seems to be out of sync. Tried updating the schema and doing a pull. But this seems to update the backend schema, resolvers etc. Had to delete the awsmobile/.awsmobile/#current-backend-info folder, edit the backend/schema.graphql and resolvers.json files and do a push. Sometimes the console does not show the updated changes and needs to be refreshed after a push operation. To be sure, try closing and opening a new console.

```graphql
    type AllPCRs
    {
    pcrs: [PCRMeasurement]!
    }
    
    type DeviceMeasurement
    {
        id: ID!
        thing_name: String!
        device_integrity: String
        listening_tcp_ports: Int
        listening_udp_ports: Int
        tcp_connections: Int
        measurement: PCRMeasurement
    }
    
    type Metrics
    {
    cpu: String
    memory: String!
    network: String
    }
    
    type Mutation
    {
    updatePCR(bootvalue: String!,pcrindex: Int!,runtimevalue: String!,status: String!,thingid: String! ): PCRMeasurement
    }
    
    type PCRMeasurement
    {
    pcrIndex: Int!
    kernel_measured_value: String!
    pcr_runtime_value: String!
    }
    
    type Query
    {
        listPCRsFor(thing_name: String! ): [PCRMeasurement]
        getDeviceMetrics(thing_name: String!): DeviceMeasurement
    }
    
    type Subscription
    {
    updatedPCR(thingid: String! ): PCRMeasurement
    } 
3. Error loading the main page from DeviceMetrics.js. The render() method would throw an error when trying to access the pcrIndex property. This was due to its parent object not being loaded. Turned out that the AppSync query was still in-flight. This is a timing issue between the query being fired and render method being called. This was resolved by https://github.com/aniruddhamaz/arc_kg_demo_082018/commit/dac2f39e02daa9088db30770ae2a8022068e4875#diff-2396a21c272dab2b820aeeac50a9de28




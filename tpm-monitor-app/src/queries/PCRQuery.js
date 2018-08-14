import gql from 'graphql-tag';

export default gql`
query {
  listPCRsFor(thingid:"ACThing") {
    pcrindex
    bootvalue
    runtimevalue
    status
  }
}
`;

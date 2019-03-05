import gql from 'graphql-tag';

export default gql`
query {
  listPCRsFor(thing_name: "ACThing") {
    thing_name
    pcr_index
    pcr_value
  }
}
`;

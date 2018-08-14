import gql from 'graphql-tag';

export default gql(`
subscription($thingid: String!) {
    updatedPCR(thingid: $thingid) {
        thingid
        pcrindex
        bootvalue
        runtimevalue
        status
    }
}
`);
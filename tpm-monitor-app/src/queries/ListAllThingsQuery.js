import gql from 'graphql-tag';

export default gql`
query {
  listThings {
    thing_name
    thing_arn
  }
}
`;

import React, {Component} from 'react';
import { StyleSheet, Text, View } from 'react-native';

class Search extends Component<Props> {
  render() {
    return (
      <View style={styles.container}>
        <Text style={styles.description}>
          Search Tab
        </Text>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  description: {
    fontSize: 20,
    backgroundColor: 'white'
  },
});

export default Search;

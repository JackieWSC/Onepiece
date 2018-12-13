/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow
 */

import React, {Component} from 'react';
import {TabBarIOS, Platform, StyleSheet, Text, View} from 'react-native';
import FetchLocation from './components/FetchLocation';
import BookList from './components/BookList';
import Featured from './components/Featured';
import Search from './components/Search';

const instructions = Platform.select({
  ios: 'Press Cmd+R to reload,\n' + 'Cmd+D or shake for dev menu',
  android:
    'Double tap R on your keyboard to reload,\n' +
    'Shake or press menu button for dev menu',
});

type Props = {};
export default class App extends Component<Props> {
  constructor(props){
    super(props);
    this.state = {
      selectedTab : 'featured'
    };
  }


  getUserLocationHandler = () => {
    console.log('Hello');
    navigator.geolocation.getCurrentPosition(position => {
      console.log(position)
    }, err => console.log(err));
  }

  render() {
    return (
      // <View style={styles.container}>
      //   <Text style={styles.welcome}>Welcome to React Native!</Text>
      //   <Text style={styles.instructions}>To get started, edit App.js</Text>
      //   <Text style={styles.instructions}>{instructions}</Text>
      //   <Text style={styles.instructions}>Jackie.Wong</Text>
      //   <FetchLocation onGetLocation={this.getUserLocationHandler} />
      // </View>
      <TabBarIOS selctedTab={this.state.selectedTab}>
        <TabBarIOS.Item
          selected={this.state.selectedTab == 'featured'}
          //icon={{uri:'featured'}}
          systemIcon="featured"
          //title="featured"
          onPress={()=> {
            this.setState({
              selectedTab:'featured'
            });
            console.log('featured');
          }}>
          <Featured/>
        </TabBarIOS.Item>
        <TabBarIOS.Item
          selected={this.state.selectedTab == 'search'}
          //icon={{uri:'search'}}
          // title="search"
          systemIcon="search"
          onPress={()=> {
            this.setState({
              selectedTab:'search'
            });
            console.log('search');
          }}>
          <Search/>
        </TabBarIOS.Item>
      </TabBarIOS>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F5FCFF',
  },
  welcome: {
    fontSize: 20,
    textAlign: 'center',
    margin: 10,
  },
  instructions: {
    textAlign: 'center',
    color: '#333333',
    marginBottom: 5,
  },
});

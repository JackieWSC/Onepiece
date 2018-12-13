import React, {Component} from 'react';
import {
  StyleSheet,
  Text,
  View,
  TextInput,
  TouchableOpacity,
 } from 'react-native';

// import {
//   Actions
// } from 'react-native-router-flux';

class Featured extends Component<Props> {
  state = {
    name: '',
  };
  render() {
    return (
      <View>
        <Text style={styles.title}>
          Enter your name:
        </Text>
        <TextInput
          style={styles.nameInput}
          placeholder='Jackie Wong'
          onChangeText={(text)=>{
            this.setState({
              name: text,
            });
          }}
          value={this.state.name}
        />
        <TouchableOpacity
          onPress={() => {
            // navigate to the second screen, and to pass it the name
            // alert(this.s tate.name)
            console.log(this.state.name)
            Actions.chat({
              name: this.state.name,
            });
            //debugger
          }}
        >
          <Text style={styles.buttonText}>
            Next
          </Text>
        </TouchableOpacity>
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
  title : {
    marginTop: 20,
    marginLeft: 20,
    fontSize: 20,
  },
  nameInput : {
    height: 40,
    borderWidth: 2,
    borderColor: 'black',
    margin: 20,
  },
  buttonText : {
    marginLeft: 20,
    fontSize: 20,
  },
});

export default Featured;

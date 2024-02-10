import React from 'react';
import { View, Text, Image, StyleSheet, Dimensions } from 'react-native';

const CenteredImageAndText = () => {
  return (
    <View style={styles.container}>
      <Image
        source="./assets/src/livent-high-resolution-logo.png" // Replace with your image URL
        style={styles.image}
      />
      <Text style={styles.text}>Viva la fica</Text>
    </View>
  );
};

const windowWidth = Dimensions.get('window').width;
const windowHeight = Dimensions.get('window').height;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  image: {
    width: windowWidth * 0.8, // Adjust as needed
    height: windowHeight * 0.3, // Adjust as needed
    resizeMode: 'contain',
    marginBottom: 20,
  },
  text: {
    fontSize: 24,
    fontWeight: 'bold',
    textAlign: 'center',
  },
});

export default CenteredImageAndText;

import { StyleSheet } from 'react-native';
const styles = StyleSheet.create({
    container: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center',
      backgroundColor: '#f5f5f5',
    },
    title: {
      fontSize: 24,
      marginBottom: 20,
    },
  
    text: {
      fontSize: 14, 
      color: "white", 
      marginTop:20, 
    }, 
    textInput: {
      borderWidth: 1, 
      borderColor: 'gray',
      padding: 10,
      width : '80%', 
      marginTop:30, 
      borderRadius:30,
      backgroundColor: 'white',
      paddingStart:30,
    },
  
    image: {
      width: 300.,  // Ancho de la imagen
      height: 200,  // Altura de la imagen
    },
  
  });
  export default styles;
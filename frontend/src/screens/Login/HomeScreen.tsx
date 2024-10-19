import React from 'react';
import { View, Text, StyleSheet,TextInput, Image, TouchableOpacity} from 'react-native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../navigation/AppNavigator';
import LoginButton from '../../componentes/loginButton';
import styles from './styles';
type HomeScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Home'>;

type Props = {
  navigation: HomeScreenNavigationProp;
};

const HomeScreen: React.FC<Props> = ({ navigation}) => {
  return (
    <View style={styles.container}>
  <Image
    source={require('../../recursos/Images/LOGO_PAPILON_VERTICAL.png')}  // Ruta correcta
    style={styles.image}
  />
      <TextInput
        placeholder='Cédula'
        style={styles.textInput}
      />
      <TextInput
        placeholder='Contraseña'
        style={styles.textInput}

      />
      {/* <TouchableOpacity
        style={[styles.primaryButton, styles.primaryButton]} // Combina estilos base con primario
        onPress={() => navigation.navigate('Welcome')}
      >
        <Text style={styles.text}>Ir a la </Text>
      </TouchableOpacity>  */}
      
      {/* <Button 
        title="Iniciar sesión"
        onPress={() => navigation.navigate('Welcome')}///plantilla que lleva a welcomec
      />

      <Button 
        title="Registrarse"
        onPress={() => navigation.navigate('Welcome')}///plantilla que lleva a welcomec
      /> */}
      <LoginButton 
        title="Iniciar Sesión" 
        onPress={() => navigation.navigate('Welcome')}///plantilla que lleva a welcomec
        backgroundColor="#F26538" 
        textColor="#fff" 
        borderRadius={30} 

      />
      <LoginButton 
        title="Registrarse" 
        onPress={() => console.log('Login pressed')} 
        backgroundColor="#EEC21B" 
        textColor="#fff" 
        borderRadius={30} 
      />

    </View>
  );
};


export default HomeScreen;
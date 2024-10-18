import React from 'react'
import { createStackNavigator } from '@react-navigation/stack';
import HomeScreen from '../screens/Login/HomeScreen'
import WelcomeScreen from '../screens/WelcomeScreen';
import UserList from '../screens/UserList';
import LoginScreen from '../screens/Login/LoginScreen';
export type RootStackParamList = {
    Home: undefined;
    Welcome: undefined;
    User : undefined,
    Login: undefined
}

const Stack = createStackNavigator<RootStackParamList>();

const homeScreenOptions = {
  title: '',         // El título estará vacío
  headerShown: false // No mostrar el encabezado
};
export default function AppNavigator() {
  return (
    <Stack.Navigator initialRouteName="Login">
      <Stack.Screen name="Home" component={HomeScreen}  options={ homeScreenOptions} />       
      <Stack.Screen name ="Login" component={LoginScreen} options={homeScreenOptions}/>
      <Stack.Screen name = "Welcome" component={WelcomeScreen} options={homeScreenOptions}/>
      <Stack.Screen name= "User" component={UserList} options={homeScreenOptions}/>
          </Stack.Navigator>
  )
}


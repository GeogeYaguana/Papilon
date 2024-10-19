import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';
import { getUsers, User } from '../services/apiContext';

const UserList: React.FC = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const data = await getUsers();
        console.log(data);
        setUsers(data);
      } catch (error) {
        console.error('Error fetching users:', error);
        setError('Error al obtener los usuarios.'); // Manejamos el error también en el estado
      }
    };

    fetchUsers();
  }, []); // Dependencias vacías para que se ejecute una vez al montar el componente

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Lista de Usuarios</Text>
      {error ? ( // Si hay un error, mostrar el mensaje
        <Text style={styles.error}>{error}</Text>
      ) : (
        <FlatList
          data={users}
          keyExtractor={(item) => item.id_usuario ? item.id_usuario.toString() : Math.random().toString()} // Maneja id undefined
          renderItem={({ item }) => (
            <View style={styles.userItem}>
              <Text>Nombre: {item.nombre}</Text>
              <Text>Email: {item.correo}</Text>
            </View>
          )}
        />
      )}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    marginBottom: 20,
  },
  userItem: {
    padding: 15,
    borderBottomWidth: 1,
    borderBottomColor: '#ddd',
  },
  error: {
    color: 'red',
    fontSize: 18,
    marginTop: 20,
  },
});

export default UserList;

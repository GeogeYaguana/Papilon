import { AxiosInstance } from 'axios';

/**
 * Servicio para obtener la lista de usuarios
 * @param apiClient Instancia de Axios configurada
 * @returns Lista de usuarios
 */
export const fetchUsers = async (apiClient: AxiosInstance): Promise<any[]> => {
  try {
    const response = await apiClient.get('/users'); // Ajusta la ruta según tu API Flask
    return response.data; // Retorna los datos de los usuarios
  } catch (error) {
    console.error('Error al obtener usuarios:', error);
    throw error; // Lanza el error para que sea manejado en el componente
  }
};

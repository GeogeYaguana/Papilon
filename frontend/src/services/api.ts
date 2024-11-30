import axios, { AxiosInstance } from 'axios';

/**
 * Crea una instancia de Axios configurada con un interceptor para el JWT
 * @param baseUrl La URL base de la API (sin el puerto)
 * @param port El puerto del servidor
 * @returns Una instancia de Axios configurada
 */
export const createApiClient = (baseUrl: string, port: number): AxiosInstance => {
  const apiClient = axios.create({
    baseURL: `${baseUrl}:${port}`,
    timeout: 5000,
    headers: {
      'Content-Type': 'application/json',
    },
  });

  // Interceptor para agregar el JWT a las cabeceras si está presente
  apiClient.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('token'); // Obtén el JWT desde el almacenamiento local
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`; // Agrega el token a las cabeceras
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  return apiClient;
};


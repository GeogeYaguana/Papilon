import { createApiClient } from './api';

const apiClient = createApiClient('http://localhost', 5000);
/**
 * Obtiene el token JWT almacenado en el almacenamiento local
 * @returns El token JWT si está presente, o null
 */
const getToken = (): string | null => {
  return localStorage.getItem('token');
};

/**
 * Almacena el token JWT en el almacenamiento local
 * @param token El token JWT a almacenar
 */
const setToken = (token: string): void => {
  localStorage.setItem('token', token);
};

/**
 * Elimina el token JWT del almacenamiento local
 */
const removeToken = (): void => {
  localStorage.removeItem('token');
};

/**
 * Verifica si el usuario está autenticado
 * @returns true si el usuario tiene un token válido, de lo contrario false
 */
const isAuthenticated = (): boolean => {
  return !!getToken();
};

/**
 * Realiza el inicio de sesión y obtiene el token JWT y el mensaje.
 * @param usuario_nombre Nombre de usuario
 * @param password Contraseña
 * @returns Objeto con el token JWT y el mensaje
 */
export const login = async (usuario_nombre: string, password: string): Promise<{ token: string; message: string }> => {
  try {
    // Realiza la solicitud POST al endpoint /login
    const response = await apiClient.post('/login', { usuario_nombre, password });
    
    // Verifica que el backend retorne un token y un mensaje
    if (response.data && response.data.token && response.data.message) {
      console.log(response);
      const { token, message } = response.data;
      setToken(token); // Almacenar el token
      return { token, message };
    } else {
      throw new Error('Respuesta inesperada del servidor');
    }
  } catch (error) {
    console.error('Error en login:', error);
    throw new Error('Credenciales inválidas o error en el servidor');
  }
};

/**
 * Cierra la sesión eliminando el token JWT
 */
export const logout = (): void => {
  removeToken(); // Elimina el token cuando se cierra la sesión
};

/**
 * Obtiene el token JWT actual
 * @returns El token JWT si está presente, o null
 */
export const getCurrentToken = (): string | null => {
  return getToken();
};

/**
 * Verifica si el usuario está autenticado
 * @returns true si el usuario tiene un token válido
 */
export const checkAuth = (): boolean => {
  return isAuthenticated();
};

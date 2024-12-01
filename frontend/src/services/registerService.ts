import { createApiClient } from './api';

const apiClient = createApiClient('http://localhost', 5000);

/**
 * Realiza el registro de un nuevo usuario en el sistema.
 * @param userData Datos del usuario para el registro
 * @returns Objeto con un mensaje de éxito o error
 */
export const register = async (userData: {
  nombre: string;
  usuario_nombre: string;
  password: string;
  correo: string;
  tipo_usuario: string;
  url_imagen?: string;
  telefono?: string;
}): Promise<{ message: string }> => {
  try {
    const response = await apiClient.post('/usuario', userData);

    // Verificar respuesta exitosa
    if (response.status === 201) {
      return { message: 'Usuario registrado exitosamente.' };
    } else {
      throw new Error(response.data.error || 'Error inesperado al registrar.');
    }
  } catch (error: any) {
    console.error('Error en register:', error);
    throw new Error(error.response?.data?.error || 'Error en el servidor.');
  }
};

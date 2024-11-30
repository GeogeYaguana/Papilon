import { login } from '../../services/authService';
import { createApiClient } from '../../services/api';

// Mock del apiClient
jest.mock('../../services/api', () => ({
  createApiClient: jest.fn(),
}));

describe('login', () => {
  const mockApiClient = {
    post: jest.fn(),
  };

  beforeAll(() => {
    // Aseguramos que el mock devuelva el apiClient simulado
    (createApiClient as jest.Mock).mockReturnValue(mockApiClient);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('debe retornar token y mensaje cuando el inicio de sesión es exitoso', async () => {
    // Configuración del mock para un inicio de sesión exitoso
    const mockResponse = {
      data: {
        token: 'mock-token',
        message: 'Inicio de sesión exitoso',
      },
    };
    mockApiClient.post.mockResolvedValue(mockResponse);

    const result = await login('juanperez', 'password123');

    expect(mockApiClient.post).toHaveBeenCalledWith('/login', {
      usuario_nombre: 'juanperez',
      password: 'password123',
    });
    expect(result).toEqual({
      token: 'mock-token',
      message: 'Inicio de sesión exitoso',
    });
  });

  it('debe lanzar un error cuando las credenciales son inválidas', async () => {
    // Configuración del mock para credenciales inválidas
    const mockError = {
      response: {
        status: 401,
        data: { message: 'Credenciales inválidas' },
      },
    };
    mockApiClient.post.mockRejectedValue(mockError);

    await expect(login('juanperez', 'wrongpassword')).rejects.toThrow(
      'Credenciales inválidas o error en el servidor'
    );
    expect(mockApiClient.post).toHaveBeenCalledWith('/login', {
      usuario_nombre: 'juanperez',
      password: 'wrongpassword',
    });
  });

  it('debe lanzar un error cuando la respuesta no contiene token o mensaje', async () => {
    // Configuración del mock para una respuesta inesperada
    const mockResponse = {
      data: {
        token: null,
        message: null,
      },
    };
    mockApiClient.post.mockResolvedValue(mockResponse);

    await expect(login('juanperez', 'password123')).rejects.toThrow(
      'Respuesta inesperada del servidor'
    );
    expect(mockApiClient.post).toHaveBeenCalledWith('/login', {
      usuario_nombre: 'juanperez',
      password: 'password123',
    });
  });

  it('debe manejar errores del servidor', async () => {
    // Configuración del mock para un error del servidor
    const mockError = new Error('Error de conexión');
    mockApiClient.post.mockRejectedValue(mockError);

    await expect(login('juanperez', 'password123')).rejects.toThrow(
      'Credenciales inválidas o error en el servidor'
    );
    expect(mockApiClient.post).toHaveBeenCalledWith('/login', {
      usuario_nombre: 'juanperez',
      password: 'password123',
    });
  });
});

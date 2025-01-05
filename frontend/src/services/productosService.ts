import { api } from './api';

// Obtener todos los productos
export const getProductos = async () => {
  const response = await api.get('/productos');
  return response.data;
};

// Obtener un producto por ID
export const getProductoById = async (id: number) => {
  const response = await api.get(`/producto/${id}`);
  return response.data;
};

// Crear un producto
export const createProducto = async (producto: any) => {
  const response = await api.post('/producto', producto);
  return response.data;
};

// Actualizar un producto
export const updateProducto = async (id: number, producto: any) => {
  const response = await api.put(`/producto/${id}`, producto);
  return response.data;
};

// Eliminar un producto
export const deleteProducto = async (id: number) => {
  const response = await api.delete(`/producto/${id}`);
  return response.data;
};

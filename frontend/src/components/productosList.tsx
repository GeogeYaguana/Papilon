import React, { useEffect, useState } from 'react';
import { getProductos } from '../services/productosService';

const ProductosList = () => {
  const [productos, setProductos] = useState([]);

  useEffect(() => {
    const fetchProductos = async () => {
      try {
        const data = await getProductos();
        setProductos(data);
      } catch (error) {
        console.error('Error al obtener productos:', error);
      }
    };

    fetchProductos();
  }, []);

  return (
    <div>
      <h1>Lista de Productos</h1>
      <ul>
        {productos.map((producto: any) => (
          <li key={producto.id_producto}>{producto.nombre}</li>
        ))}
      </ul>
    </div>
  );
};

export default ProductosList;

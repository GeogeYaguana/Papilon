import React, { useEffect, useState } from 'react';
import { Box, Button, Typography } from '@mui/material';
import Sidebar from '../components/sidebar';
import ProductCard from '../components/productCard';
import { getProductos } from '../services/productosService'; // Asegúrate de la ruta correcta

interface Product {
  id_producto: number;
  nombre: string;
  precio: number;
  descuento: number;
  foto_url: string;
}

const Dashboard = () => {
  const [productos, setProductos] = useState<Product[]>([]);
  
  useEffect(() => {
    const fetchProductos = async () => {
      try {
        const data = await getProductos();
        setProductos(data);
      } catch (error) {
        console.error('Error al obtener los productos:', error);
      }
    };

    fetchProductos();
  }, []);

  return (
    <Box display="flex" height="100vh">
      <Sidebar />
      <Box flex={1} bgcolor="#f6f6f6">
        <Box bgcolor="#ffa500" p={2}>
          <Typography variant="h4" color="white">
            Bienvenido al Dashboard
          </Typography>
        </Box>
        <Box display="flex" justifyContent="space-around" p={2}>
          <Button variant="contained" color="primary">Crear Producto</Button>
          <Button variant="contained" color="warning">Ver Canjes</Button>
          <Button variant="contained" color="success">Registrar Factura</Button>
          <Button variant="contained" color="info">Ver Facturas</Button>
          <Button variant="contained" color="error">Cerrar Sesión</Button>
        </Box>
        <Box display="grid" gridTemplateColumns="repeat(auto-fill, minmax(250px, 1fr))" gap={3} p={3}>
          {productos.map((producto) => (
            <ProductCard key={producto.id_producto} product={producto} />
          ))}
        </Box>
      </Box>
    </Box>
  );
};

export default Dashboard;

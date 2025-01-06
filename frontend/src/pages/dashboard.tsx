import React, { useEffect, useState } from 'react'; 
import { Box, Button, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import Sidebar from '../components/sidebar';
import ProductCard from '../components/productCard';
import { getProductos } from '../services/productosService'; // Ensure the correct path

interface Product {
  id_producto: number;
  nombre: string;
  precio: number;
  descuento: number;
  foto_url: string;
}

const Dashboard = () => {
  const [productos, setProductos] = useState<Product[]>([]);
  const navigate = useNavigate(); // Initialize useNavigate

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

  const routes = [
    { text: 'Crear Producto', path: '/dashboard', color: 'primary' },
    { text: 'Ver Canjes', path: '/canjes', color: 'warning' },
    { text: 'Registrar Factura', path: '/registrar-facturas', color: 'success' },
    { text: 'Ver Facturas', path: '/ver-facturas', color: 'info' },
    { text: 'Cerrar Sesión', path: '/logout', color: 'error' },
  ];

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
          {routes.map((route, index) => (
            <Button
              key={index}
              variant="contained"
              color={route.color as 'primary' | 'warning' | 'success' | 'info' | 'error'}
              onClick={() => navigate(route.path)}
            >
              {route.text}
            </Button>
          ))}
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

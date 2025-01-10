import React, { useState } from 'react';
import { Box, Button, TextField, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { createProducto } from '../services/productosService'; // Asegúrate de tener este servicio

const CreateProduct = () => {
  const [nombre, setNombre] = useState('');
  const [precio, setPrecio] = useState<number | ''>('');
  const [descuento, setDescuento] = useState<number | ''>('');
  const [fotoUrl, setFotoUrl] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!nombre || precio === '' || descuento === '' || !fotoUrl) {
      alert('Por favor, completa todos los campos.');
      return;
    }

    try {
      await createProducto({
        nombre,
        precio: Number(precio),
        descuento: Number(descuento),
        foto_url: fotoUrl,
      });
      alert('Producto creado exitosamente.');
      navigate('/dashboard'); // Redirige al Dashboard
    } catch (error) {
      console.error('Error al crear el producto:', error);
      alert('Ocurrió un error al crear el producto.');
    }
  };

  return (
    <Box display="flex" flexDirection="column" alignItems="center" p={4}>
      <Typography variant="h4" mb={3}>
        Crear Producto
      </Typography>
      <form onSubmit={handleSubmit}>
        <Box display="flex" flexDirection="column" gap={2} width="400px">
          <TextField
            label="Nombre"
            variant="outlined"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
          />
          <TextField
            label="Precio"
            variant="outlined"
            type="number"
            value={precio}
            onChange={(e) => setPrecio(Number(e.target.value))}
          />
          <TextField
            label="Descuento (%)"
            variant="outlined"
            type="number"
            value={descuento}
            onChange={(e) => setDescuento(Number(e.target.value))}
          />
          <TextField
            label="URL de la Foto"
            variant="outlined"
            value={fotoUrl}
            onChange={(e) => setFotoUrl(e.target.value)}
          />
          <Button type="submit" variant="contained" color="primary">
            Crear Producto
          </Button>
        </Box>
      </form>
    </Box>
  );
};

export default CreateProduct;

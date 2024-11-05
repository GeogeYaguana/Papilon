import React from 'react';
import CardContainer from '../../components/CardContainer';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';

function ProductosFidelizados() {
  const cards = Array(6).fill({
    title: 'Producto Ejemplo',
    image: 'https://via.placeholder.com/300x200', // Imagen de muestra de Lorem Ipsum
    price: 10.00,
    points: 100,
    altText: 'Producto ejemplo',
  });

  return (
    <Box sx={{ padding: '20px' }}>
      {/* Contenedor del título y el botón */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <Button 
          variant="contained" 
          sx={{ 
            backgroundColor: 'yellow', 
            color: 'black', 
            '&:hover': { backgroundColor: '#FFD700' }
          }}
        >
          Agregar Producto
        </Button>
      </Box>

      {/* Contenedor de las tarjetas con scroll horizontal */}
      <Box 
        sx={{ 
          display: 'flex', 
          overflowX: 'auto', 
          padding: '10px', 
          '&::-webkit-scrollbar': { display: 'none' }
        }}
      >
        {cards.map((card, index) => (
          <Box key={index} sx={{ minWidth: 300, marginRight: '16px' }}>
            <CardContainer 
              title={card.title}
              image={card.image}
              price={card.price}
              points={card.points}
              altText={card.altText}
            />
          </Box>
        ))}
      </Box>
    </Box>
  );
}

export default ProductosFidelizados;

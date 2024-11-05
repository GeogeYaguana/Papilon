import React from 'react';
import CardContainer from '../../components/CardContainer';
import Box from '@mui/material/Box';

function ProductosFidelizados() {
  const cards = Array(6).fill({
    title: 'Producto Ejemplo',
    image: 'https://via.placeholder.com/300x200', // Imagen de muestra de Lorem Ipsum
    price: 10.00,
    points: 100,
    altText: 'Producto ejemplo',
  });

  return (
    <Box 
      sx={{ 
        display: 'flex', 
        overflowX: 'auto', 
        padding: '20px', 
        '&::-webkit-scrollbar': { display: 'none' } // Oculta la barra de desplazamiento en navegadores Webkit
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
  );
}

export default ProductosFidelizados;

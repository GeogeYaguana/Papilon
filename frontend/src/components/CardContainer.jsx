import React from 'react';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';

function CardContainer({ title, image, price, points, altText }) {
  return (
    <Card sx={{ maxWidth: 300, height: 400, margin: '0 10px' }}>
      <CardMedia
        sx={{ height: 200 }}
        image={image}
        title={altText}
      />
      <CardContent>
        <Typography gutterBottom variant="h5" component="div">
          {title}
        </Typography>
        <Typography variant="body2" sx={{ color: 'text.secondary' }}>
          ${price}
        </Typography>
        
        <Typography variant="body2" sx={{ color: 'text.secondary' }}>
          ⭐ {points} pts
        </Typography>
      </CardContent>
      <CardActions sx={{ justifyContent: 'space-between', marginBottom: 2 }}>
        <Button
          size="small"
          sx={{
            borderRadius: '20px',
            backgroundColor: 'yellow',
            color: 'black',
            '&:hover': { backgroundColor: '#FFD700' },
          }}
        >
          Editar Producto
        </Button>
        <Button
          size="small"
          sx={{
            borderRadius: '20px',
            backgroundColor: 'pink',
            color: 'black',
            '&:hover': { backgroundColor: '#FF69B4' },
          }}
        >
          Eliminar Producto
        </Button>
      </CardActions>
    </Card>
  );
}

export default CardContainer;

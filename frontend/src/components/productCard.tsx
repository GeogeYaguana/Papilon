import React from 'react';
import { Card, CardContent, CardMedia, Typography } from '@mui/material';

interface Product {
  id_producto: number;
  nombre: string;
  precio: number;
  descuento: number;
  foto_url: string;
}

interface ProductCardProps {
  product: Product;
}

const ProductCard: React.FC<ProductCardProps> = ({ product }) => {
  return (
    <Card>
      <CardMedia
        component="img"
        height="140"
        image={product.foto_url}
        alt={product.nombre}
      />
      <CardContent>
        <Typography variant="h6">{product.nombre}</Typography>
        <Typography variant="body2" color="textSecondary">
          Precio: ${product.precio.toFixed(2)}
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Descuento: {product.descuento}%
        </Typography>
      </CardContent>
    </Card>
  );
};

export default ProductCard;

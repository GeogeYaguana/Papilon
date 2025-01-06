// src/pages/Facturas.tsx
import React from 'react';
import { Box, Button, Typography } from '@mui/material';
import Sidebar from '../components/sidebar';
import '../assets/styles/facturas.css';

const Facturas: React.FC = () => {
  const facturas = [
    { id: 48, total: 2401.0, estado: 'pagada' },
    { id: 53, total: 1200.5, estado: 'pendiente' },
    { id: 54, total: 1200.5, estado: 'pendiente' },
    { id: 44, total: 1200.5, estado: 'anulada' },
    { id: 46, total: 1200.5, estado: 'anulada' },
    { id: 56, total: 1200.5, estado: 'pagada' },
    { id: 55, total: 1200.5, estado: 'reembolsada' },
    { id: 57, total: 450.0, estado: 'anulada' },
  ];

  return (
    <Box display="flex" height="100vh">
      <Sidebar />
      <Box flex={1}
      bgcolor="#f6f6f6"
      p={2} // Adds padding inside the Box
      m={2} // Adds margin outside the Box
      borderRadius={2} // Rounds the corners
      >
        <div className="container-facturas">
          <h1 className="title-facturas">Lista de Facturas</h1>
          <table className="table-facturas">
            <thead>
              <tr>
                <th>ID Factura</th>
                <th>Total</th>
                <th>Estado</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {facturas.map((factura) => (
                <tr key={factura.id}>
                  <td>{factura.id}</td>
                  <td>${factura.total.toFixed(2)}</td>
                  <td>{factura.estado}</td>
                  <td>
                    <button
                      className="state-button"
                      onClick={() => alert(`Cambiar estado de factura ${factura.id}`)}
                    >
                      Cambiar Estado
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Box>
    </Box>
  );
};

export default Facturas;

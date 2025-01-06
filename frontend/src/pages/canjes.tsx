// src/pages/Canjes.tsx
import React from 'react';
import { Box, Typography } from '@mui/material';
import Sidebar from '../components/sidebar';
import '../assets/styles/canjes.css';

const Canjes: React.FC = () => {
  const error = true; // Simula un error cargando canjes
  const canjes = []; // Lista de canjes, vacía para este caso

  return (
    <Box display="flex" height="100vh">
      <Sidebar />
      <Box flex={1}
      bgcolor="#f6f6f6"
      p={2} // Adds padding inside the Box
      m={2} // Adds margin outside the Box
      borderRadius={2} // Rounds the corners
      >
        <div className="canjes-container">
          <h1 className="canjes-title">Lista de Canjes</h1>
          {error ? (
            <div className="canjes-notfound-container">
              <p className="error-text">Error al cargar los canjes asociados al local</p>
              <p className="info-text">No se encontraron canjes</p>
            </div> 
          ) : (
            <p className="canjes-text">El siguiente es el listado de canjes</p>
          )}
          {!error && canjes.length === 0 && (
            <table className="canjes-table">
              <thead>
                <tr>
                  <th>Nombre Cliente</th>
                  <th>Fecha</th>
                  <th>Estado</th>
                  <th>Local</th>
                  <th>Detalles</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td colSpan={6} className="no-data">
                    No hay datos disponibles.
                  </td>
                </tr>
              </tbody>
            </table>
          )}
        </div>
      </Box>
    </Box>
  );
};

export default Canjes;

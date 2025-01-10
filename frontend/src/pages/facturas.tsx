import React, { useEffect, useState } from 'react';
import { Box, Typography, Button, Table, TableHead, TableRow, TableCell, TableBody, TablePagination } from '@mui/material';
import Sidebar from '../components/sidebar';

const Facturas: React.FC = () => {
  const [facturas, setFacturas] = useState<{ id: number; total: number; estado: string }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [token, setToken] = useState<string>(''); // Simula obtener el token desde la autenticación
  const [page, setPage] = useState(0); // Para la paginación
  const [rowsPerPage, setRowsPerPage] = useState(5); // Número de filas por página

  const idUsuario = 1; // Simula obtener el ID del usuario desde el contexto o autenticación

  // Cargar facturas con paginación
  useEffect(() => {
    const fetchFacturas = async () => {
      try {
        setLoading(true);
        const response = await fetch(`http://localhost:5000/facturas/usuario/${idUsuario}?page=${page}&rows=${rowsPerPage}`, {
          headers: {
            Authorization: `Bearer ${token}`, // Enviar el token en los encabezados
          },
        });
        if (!response.ok) throw new Error('Error al obtener las facturas');
        const data = await response.json();
        setFacturas(data.facturas || []);
      } catch (err) {
        console.error('Error al cargar las facturas:', err);
        setError('No se pudieron cargar las facturas. Intenta nuevamente más tarde.');
      } finally {
        setLoading(false);
      }
    };

    fetchFacturas();
  }, [idUsuario, page, rowsPerPage, token]);

  // Cambiar de página en la tabla
  const handleChangePage = (_: unknown, newPage: number) => {
    setPage(newPage);
  };

  // Cambiar número de filas por página
  const handleChangeRowsPerPage = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0); // Reiniciar la página al cambiar el número de filas
  };

  if (loading) {
    return (
      <Box display="flex" height="100vh">
        <Sidebar />
        <Box flex={1} bgcolor="#f6f6f6" p={4}>
          <Typography variant="h5">Cargando facturas...</Typography>
        </Box>
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" height="100vh">
        <Sidebar />
        <Box flex={1} bgcolor="#f6f6f6" p={4}>
          <Typography variant="h5" color="error">{error}</Typography>
        </Box>
      </Box>
    );
  }

  // Mostrar detalles de una factura
  const handleViewDetails = async (idFactura: number) => {
    try {
      const response = await fetch(`http://localhost:5000/facturas/${idFactura}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      if (!response.ok) throw new Error('Error al obtener los detalles de la factura');
      const data = await response.json();
      alert(`Detalles de la factura ${idFactura}: ${JSON.stringify(data, null, 2)}`);
    } catch (err) {
      console.error('Error al cargar los detalles:', err);
      setError('No se pudieron cargar los detalles. Intenta nuevamente más tarde.');
    }
  };

  return (
    <Box display="flex" height="100vh">
      <Sidebar />
      <Box flex={1} bgcolor="#f6f6f6">
        <Box bgcolor="#ffa500" p={2}>
          <Typography variant="h4" color="white">
            Bienvenido al Dashboard
          </Typography>
        </Box>
        <Box p={2}>
          <Typography variant="h5">Lista de Facturas</Typography>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>ID Factura</TableCell>
                <TableCell>Total</TableCell>
                <TableCell>Estado</TableCell>
                <TableCell>Acciones</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {facturas.map((factura) => (
                <TableRow key={factura.id}>
                  <TableCell>{factura.id}</TableCell>
                  <TableCell>${factura.total.toFixed(2)}</TableCell>
                  <TableCell>{factura.estado}</TableCell>
                  <TableCell>
                    <Button
                      variant="contained"
                      color="primary"
                      onClick={() => handleViewDetails(factura.id)}
                    >
                      Ver Detalles
                    </Button>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <TablePagination
            component="div"
            count={-1} // Cambia esto si implementas total de registros desde el backend
            page={page}
            onPageChange={handleChangePage}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={handleChangeRowsPerPage}
          />
        </Box>
      </Box>
    </Box>
  );
};

export default Facturas;

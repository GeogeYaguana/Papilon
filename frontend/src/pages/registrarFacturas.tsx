import React, { useState } from 'react'; 
import { Box, Button } from '@mui/material';
import Sidebar from '../components/sidebar';
import '../assets/styles/registrarFacturas.css';

const RegistrarFactura: React.FC = () => {
  const [detalles, setDetalles] = useState<{ producto: string; cantidad: number }[]>([]);
  const [total, setTotal] = useState(0);
  const [clienteId, setClienteId] = useState<string>('');
  const [estado, setEstado] = useState<string>('');

  const handleAddDetail = () => {
    const producto = (document.getElementById('producto') as HTMLSelectElement).value;
    const cantidad = parseInt((document.getElementById('cantidad') as HTMLInputElement).value, 10);

    if (!producto) {
      alert('Por favor, selecciona un producto antes de añadir un detalle.');
      return;
    }

    if (cantidad <= 0) {
      alert('Por favor, ingresa una cantidad válida.');
      return;
    }

    setDetalles([...detalles, { producto, cantidad }]);
    setTotal(total + cantidad * 100); // Example: Each product is $100.
  };

  const handleSubmit = async () => {
    if (!clienteId || !estado || detalles.length === 0) {
      alert('Por favor completa todos los campos y agrega al menos un detalle.');
      return;
    }

    const facturaData = {
      id_cliente: clienteId,
      estado,
      total,
      detalle_facturas: detalles.map((detalle) => ({
        id_producto: detalle.producto, // Aquí deberías usar el ID real del producto.
        precio_unitario: 100, // Ejemplo: precio fijo, deberías obtenerlo dinámicamente.
        cantidad: detalle.cantidad,
      })),
      id_usuario_local: 1, // Cambia esto por el ID del usuario local actual.
    };

    try {
      const response = await fetch('http://tu-backend.com/facturas', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(facturaData),
      });

      if (!response.ok) {
        throw new Error('Error al registrar la factura');
      }

      const data = await response.json();
      alert('Factura registrada exitosamente');
      console.log('Factura registrada:', data);

      // Resetear el formulario
      setClienteId('');
      setEstado('');
      setDetalles([]);
      setTotal(0);
    } catch (error) {
      console.error('Error al registrar la factura:', error);
      alert('Ocurrió un error al registrar la factura.');
    }
  };

  return (
    <Box display="flex" height="100vh">
      <Sidebar />
      <Box
        flex={1}
        bgcolor="#f6f6f6"
        p={2}
        m={2}
        borderRadius={2}
        display="flex"
        justifyContent="center"
      >
        <div className="registrof-container">
          <h1 className="registrof-title">Registrar Factura</h1>
          <form>
            <div className="form-group">
              <label htmlFor="clienteId">ID del Cliente</label>
              <input
                type="text"
                id="clienteId"
                className="form-control"
                placeholder="Ingresa el ID del cliente"
                value={clienteId}
                onChange={(e) => setClienteId(e.target.value)}
                style={{ width: "100%" }}
              />
            </div>
            <div className="form-group">
              <label htmlFor="estado">Estado</label>
              <select
                id="estado"
                className="form-control"
                value={estado}
                onChange={(e) => setEstado(e.target.value)}
              >
                <option value="">-- Selecciona un estado --</option>
                <option value="pagada">Pagada</option>
                <option value="pendiente">Pendiente</option>
                <option value="anulada">Anulada</option>
                <option value="reembolsada">Reembolsada</option>
              </select>
            </div>
            <h2>Detalles de Factura</h2>
            <div className="form-group" style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <label htmlFor="producto" style={{ flex: 1, textAlign: "left" }}>Producto</label>
                <label htmlFor="cantidad" style={{ flex: 1, textAlign: "left" }}>Cantidad</label>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between" }}>
                <select id="producto" className="form-control" style={{ flex: 1, marginRight: "10px" }}>
                  <option value="">-- Selecciona un producto --</option>
                  <option value="Producto A">Producto A</option>
                  <option value="Producto B">Producto B</option>
                  <option value="Producto C">Producto C</option>
                </select>
                <input
                  type="number"
                  id="cantidad"
                  className="form-control"
                  style={{ flex: 1 }}
                  min="1"
                  defaultValue={1}
                />
              </div>
            </div>
            <div style={{ display: "flex", justifyContent: "center", margin: "20px 0" }}>
              <Button variant="contained" color="primary" onClick={handleAddDetail}>
                Añadir Detalle
              </Button>
            </div>
          </form>
          <h3>Total: ${total.toFixed(2)}</h3>
          <div
            style={{
              maxHeight: "200px",
              overflowY: "auto",
              padding: "10px",
            }}
          >
            <ul>
              {detalles.map((detalle, index) => (
                <li key={index}>
                  {detalle.producto} - {detalle.cantidad} unidades
                </li>
              ))}
            </ul>
          </div>
          <div style={{ display: "flex", justifyContent: "center", margin: "20px 0" }}>
            <Button variant="contained" color="secondary" onClick={handleSubmit}>
              Registrar Factura
            </Button>
          </div>
        </div>
      </Box>
    </Box>
  );
};

export default RegistrarFactura;

import React from 'react';
import { Box, List, ListItem, ListItemText, Typography } from '@mui/material';

const Sidebar = () => {
  return (
    <Box width="240px" bgcolor="#fff" p={2} boxShadow={2}>
      <Typography variant="h5" color="primary" mb={2}>Papilon</Typography>
      <List>
        {['Productos', 'Ver Canjes', 'Registrar Facturas', 'Ver Facturas'].map((text, index) => (
          <ListItem component="button" key={text}>
            <ListItemText primary={text} />
           </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default Sidebar;

import React from 'react';
import { Box, List, ListItem, ListItemText, Typography } from '@mui/material';
import { Link } from 'react-router-dom';
import { styled } from '@mui/system';

const StyledLink = styled(Link)({
  textDecoration: 'none',
  color: 'inherit',
  display: 'flex',
  width: '100%',
});

const Sidebar = () => {
  return (
    <Box width="240px" bgcolor="#fff" p={2} boxShadow={2}>
      <List>
        {[
          { text: 'Productos', path: '/dashboard' },
          { text: 'Ver Canjes', path: '/canjes' },
          { text: 'Registrar Facturas', path: '/registrar-facturas' },
          { text: 'Ver Facturas', path: '/ver-facturas' },
        ].map(({ text, path }) => (
          <ListItem key={text}>
            <StyledLink to={path}>
              <ListItemText primary={text} />
            </StyledLink>
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default Sidebar;

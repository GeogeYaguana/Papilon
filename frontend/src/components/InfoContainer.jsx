import React from 'react';
import { Box, Grid, Typography, Icon } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle'; // Puedes cambiar el icono según tu preferencia

interface InfoContainerProps {
  icon: React.ReactNode;
  number: number;
  label: string;
}

const InfoContainer: React.FC<InfoContainerProps> = ({ icon, number, label }) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        padding: 2,
        borderRadius: 1,
        border: '1px solid #ddd',
        width: '100%',
        textAlign: 'center',
      }}
    >
      <Icon sx={{ fontSize: 40 }}>{icon}</Icon>
      <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
        {number}
      </Typography>
      <Typography variant="subtitle1" color="textSecondary">
        {label}
      </Typography>
    </Box>
  );
};

export default InfoContainer;

import * as React from "react";
import { extendTheme, styled } from "@mui/material/styles";
import DashboardIcon from "@mui/icons-material/Dashboard";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";
import BarChartIcon from "@mui/icons-material/BarChart";
import DescriptionIcon from "@mui/icons-material/Description";
import LayersIcon from "@mui/icons-material/Layers";
import { AppProvider, Navigation, Router } from "@toolpad/core/AppProvider";
import { DashboardLayout } from "@toolpad/core/DashboardLayout";
import { PageContainer } from "@toolpad/core/PageContainer";
import Grid2 from "@mui/material/Grid2"; // Nueva importación
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Container from "@mui/material/Container";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import CardActionArea from "@mui/material/CardActionArea";
import { Card, CardMedia, CardActions, Button } from "@mui/material";
import Barchart from "../../testCharts/Barchart";
import Piechart from "../../testCharts/Piechart";
import ProductosFidelizados from "./ProductosFidelizados";
import Productos from "./Productos";




const NAVIGATION: Navigation = [
  { kind: "header", title: "Main items" },
  { segment: "dashboard", title: "Dashboard", icon: <DashboardIcon /> },
  { segment: "fidelizados", title: "Catálogo Fidelización", icon: <ShoppingCartIcon /> },
  { segment: "catalog", title: "Catálogo Productos", icon: <DashboardIcon /> },
  { kind: "divider" },


];

const demoTheme = extendTheme({
  colorSchemes: { light: true, dark: true },
  colorSchemeSelector: "class",
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 600,
      lg: 1200,
      xl: 1536,
    },
  },
});

function useDemoRouter(initialPath: string): Router {
  const [pathname, setPathname] = React.useState(initialPath);

  const router = React.useMemo(() => {
    return {
      pathname,
      searchParams: new URLSearchParams(),
      navigate: (path: string | URL) => setPathname(String(path)),
    };
  }, [pathname]);

  return router;
}

function DashboardContent() {
  return (




    <Grid2 container spacing={2} sx={{ justifyContent: 'space-between'}}>
      <Grid2 sx={{ gridColumn: { xs: "span 12", sm: "span 4" } }}>
        <Card sx={{ maxWidth: 300 }}>
          <CardActionArea>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                153
              </Typography>
              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                Clientes Atendidos
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      </Grid2>
      <Grid2 sx={{ gridColumn: { xs: "span 12", sm: "span 4" } }}>
        <Card sx={{ maxWidth: 345 }}>
          <CardActionArea>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                25
              </Typography>
              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                Clientes Fidelizados
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      </Grid2>
      <Grid2 sx={{ gridColumn: { xs: "span 12", sm: "span 4" } }}>
        <Card sx={{ maxWidth: 345 }}>
          <CardActionArea>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                10000
              </Typography>
              <Typography variant="body2" sx={{ color: "text.secondary" }}>
                Total de puntos de fidelizacion otorgados
              </Typography>
            </CardContent>
          </CardActionArea>
        </Card>
      </Grid2>
      <Grid2 size={8}>

          <Card>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Productos Canjeados
              </Typography>
              <Typography
                variant="body2"
                sx={{ color: "text.secondary" }}
              ></Typography>
              <Barchart />
            </CardContent>
          </Card>

      </Grid2>
      <Grid2 size={4}>
          <Card>
            <CardContent>
              <Typography gutterBottom variant="h5" component="div">
                Productos más vendidos
              </Typography>
              <Typography
                variant="body2"
                sx={{ color: "text.secondary" }}
              ></Typography>
              <Piechart />
            </CardContent>
          </Card>

      </Grid2>
    </Grid2>
  );
}



function ReportsContent() {
  return <Box>Contenido de Reportes</Box>;
}

export default function DashboardMain(props: any) {
  const { window } = props;
  const router = useDemoRouter("/dashboard");

  const renderContent = () => {
    switch (router.pathname) {
      case "/dashboard":
        return <DashboardContent />;
      case "/fidelizados":
        return <ProductosFidelizados />;
        case "/catalog":
          return <Productos />;  
      case "/reports/sales":
      case "/reports/traffic":
        return <ReportsContent />;
      default:
        return <Box>Seleccione una opción</Box>;
    }
  };

  return (
    <AppProvider
      navigation={NAVIGATION}
      router={router}
      theme={demoTheme}
      window={window}
    >
      <DashboardLayout>
        <PageContainer>
          <Box sx={{ padding: 2, maxWidth: 1200, margin: "auto" }}>
            {renderContent()}
          </Box>
        </PageContainer>
      </DashboardLayout>
    </AppProvider>
  );
}

# Papilon

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)
![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue)

## Descripción

**Papilon** es una aplicación completa que abarca una página web desarrollada con **React**, una aplicación móvil con **React Native**, un backend robusto construido con **Flask**, y una base de datos **PostgreSQL**. La arquitectura del proyecto está diseñada para ser escalable, mantenible y eficiente, utilizando **Docker** para facilitar el desarrollo y despliegue.

## Tabla de Contenidos

- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Prerequisitos](#prerequisitos)
- [Instalación](#instalación)
  - [Clonar el Repositorio](#clonar-el-repositorio)
  - [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
  - [Iniciar los Servicios con Docker](#iniciar-los-servicios-con-docker)
- [Uso](#uso)
  - [Frontend (Página Web)](#frontend-página-web)
  - [Mobile (Aplicación Móvil)](#mobile-aplicación-móvil)
  - [Backend (Flask)](#backend-flask)
  - [Base de Datos (PostgreSQL)](#base-de-datos-postgresql)
- [Pruebas](#pruebas)
  - [Pruebas del Frontend](#pruebas-del-frontend)
  - [Pruebas del Backend](#pruebas-del-backend)
- [CI/CD](#cicd)
- [Contribución](#contribución)
- [Licencia](#licencia)
- [Contacto](#contacto)

## Tecnologías Utilizadas

### Frontend
- **React** ^18.2.0
- **TypeScript** ^4.9.5
- **Redux Toolkit** ^1.9.5
- **React Router DOM** ^6.x
- **Axios** ^0.27.x
- **ESLint** ^8.50.0
- **Prettier** ^3.0.0

### Mobile
- **React Native** ^0.72.0
- **Expo** ^48.x
- **Redux Toolkit** ^1.9.5
- **React Navigation** ^6.x
- **Axios** ^0.27.x
- **ESLint** ^8.50.0
- **Prettier** ^3.0.0

### Backend
- **Python** ^3.11
- **Flask** ^2.3.2
- **Flask-RESTful** ^0.3.9
- **Flask-Cors** ^3.1.1
- **SQLAlchemy** ^2.0.x
- **psycopg2-binary** ^2.9.x
- **PyTest** ^7.4.0
- **Flake8** ^4.0.1

### Base de Datos
- **PostgreSQL** ^15.4

### Infraestructura
- **Docker** ^20.10.x
- **Docker Compose** ^3.8
- **Terraform** ^1.4.0 (opcional para infraestructura avanzada)
- **Ansible** ^2.14.0 (opcional para gestión de configuración)

### CI/CD
- **GitHub Actions**

## Estructura del Proyecto

```
mi-proyecto/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── tests/
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   ├── Dockerfile
│   └── src/
├── mobile/
│   ├── package.json
│   ├── app.json
│   ├── Dockerfile
│   └── src/
├── database/
│   └── docker-compose.yml (opcional si se gestiona desde el root)
├── docker/
│   └── (archivos de configuración adicionales)
├── .github/
│   └── workflows/
│       ├── backend.yml
│       └── frontend.yml
├── docker-compose.yml
├── .gitignore
├── README.md
└── LICENSE
```

## Prerequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu máquina:

- [Git](https://git-scm.com/)
- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Node.js](https://nodejs.org/) ^18.0.0
- [Python](https://www.python.org/) ^3.11
- [Yarn](https://yarnpkg.com/) (opcional, si prefieres usar Yarn sobre npm)

## Instalación

### Clonar el Repositorio

```bash
# Clona el repositorio
git clone https://github.com/tu-usuario/mi-proyecto.git

# Navega al directorio del proyecto
cd mi-proyecto
```

### Configuración de Variables de Entorno

Crea un archivo `.env` en el directorio raíz para almacenar las variables de entorno necesarias.

```bash
# Crear archivo .env
touch .env
```

Añade las siguientes variables al archivo `.env`:

```env
# Backend
FLASK_ENV=development
DATABASE_URL=postgresql://miusuario:mipassword@db:5432/mibasededatos

# Frontend
REACT_APP_API_URL=http://localhost:5000/api

# Mobile (si es necesario)
API_URL=http://localhost:5000/api
```

**Nota:** Asegúrate de reemplazar `miusuario`, `mipassword` y `mibasededatos` con tus credenciales reales.

### Iniciar los Servicios con Docker

Docker simplifica el despliegue y la gestión de los diferentes servicios de la aplicación.

```bash
# Iniciar todos los servicios en segundo plano
docker-compose up -d --build
```

Esto levantará los siguientes servicios:

- **PostgreSQL** en el puerto `5432`
- **Backend (Flask)** en el puerto `5000`
- **Frontend (React)** en el puerto `3000`

## Uso

### Frontend (Página Web)

Accede a la aplicación web abriendo tu navegador y navegando a [http://localhost:3000](http://localhost:3000).

#### Comandos Útiles

```bash
# Navega al directorio frontend
cd frontend

# Instalar dependencias
npm install

# Iniciar el servidor de desarrollo
npm start

# Ejecutar pruebas
npm test

# Linting
npm run lint

# Formateo de código
npm run format
```

### Mobile (Aplicación Móvil)

Para desarrollar y probar la aplicación móvil, se recomienda usar **Expo**.

#### Comandos Útiles

```bash
# Navega al directorio mobile
cd mobile

# Instalar dependencias
npm install

# Iniciar el servidor de Expo
npm start

# Abrir en Android
npm run android

# Abrir en iOS
npm run ios

# Ejecutar pruebas
npm test

# Linting
npm run lint

# Formateo de código
npm run format
```

### Backend (Flask)

El backend proporciona APIs RESTful para interactuar con el frontend y la aplicación móvil.

#### Comandos Útiles

```bash
# Navega al directorio backend
cd backend

# Crear y activar un entorno virtual (si no está activo)
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Iniciar el servidor Flask
python app.py

# Ejecutar pruebas
pytest

# Linting
flake8 .
```

### Base de Datos (PostgreSQL)

La base de datos está gestionada mediante Docker y se conecta automáticamente al backend.

#### Acceso a la Base de Datos

Puedes acceder a la base de datos usando herramientas como **pgAdmin** o **DBeaver** con las siguientes credenciales:

- **Host:** localhost
- **Puerto:** 5432
- **Usuario:** miusuario
- **Contraseña:** mipassword
- **Base de Datos:** mibasededatos

## Pruebas

### Pruebas del Frontend

El frontend utiliza **Jest** y **React Testing Library** para realizar pruebas unitarias y de integración.

#### Ejecutar Pruebas

```bash
# Navega al directorio frontend
cd frontend

# Ejecutar todas las pruebas
npm test
```

### Pruebas del Backend

El backend utiliza **PyTest** para realizar pruebas unitarias y de integración.

#### Ejecutar Pruebas

```bash
# Navega al directorio backend
cd backend

# Activar el entorno virtual
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Ejecutar todas las pruebas
pytest
```

## CI/CD

El proyecto está configurado con **GitHub Actions** para automatizar los procesos de integración continua y despliegue.

### Workflows Configurados

- **Backend CI:** Se ejecutan pruebas y verificaciones de calidad en cada push o pull request que afecte al directorio `backend/`.
- **Frontend CI:** Se ejecutan pruebas y verificaciones de calidad en cada push o pull request que afecte al directorio `frontend/`.


## Contribución

¡Contribuciones son bienvenidas! Sigue estos pasos para contribuir:

1. **Fork** el repositorio.
2. Crea una **branch** para tu feature o bugfix:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza tus **cambios** y **commit**:
   ```bash
   git commit -m "Descripción de la feature"
   ```
4. **Push** a tu fork:
   ```bash
   git push origin feature/nueva-funcionalidad
   ```
5. Abre un **Pull Request** en el repositorio original.

### Reglas de Código

- Sigue las **mejores prácticas** de codificación para cada tecnología.
- Asegúrate de que tu código pase todas las **pruebas y linters** antes de hacer commit.
- Documenta tus **cambios** y **nuevas funcionalidades** adecuadamente.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).




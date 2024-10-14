# Papilon

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Node.js](https://img.shields.io/badge/node-%3E%3D18.0.0-brightgreen)
![Python](https://img.shields.io/badge/python-%3E%3D3.11-blue)

## Descripción

El proyecto se enfoca en desarrollar una aplicación móvil y una página web destinada a
facilitar el canje de puntos de fidelización acumulados en locales afiliados por compras
realizadas. Las soluciones anteriores al problema generalmente han sido sistemas de
fidelización individuales para cada local, lo que resultaba en una falta de uniformidad y
eficiencia en la gestión de puntos y recompensas. Además, el uso de tarjetas físicas de
fidelización, propensas a pérdida y desgaste, no permitía visualizar ofertas ni canjear
puntos en tiempo real. La solución esperada es una plataforma digital interconectada que,
a través de la aplicación móvil, permitirá a los usuarios visualizar ofertas y canjear puntos
fácilmente desde cualquier ubicación. La página web proporcionará a los propietarios de
locales una herramienta robusta para gestionar productos y puntajes de fidelización, con
un sistema de permisos para garantizar la seguridad de los datos, asegurando que solo
aquellos con permisos de administrador puedan realizar cambios, que se reflejarán
automáticamente en la aplicación móvil.
## Tabla de Contenidos

- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Prerequisitos](#prerequisitos)
- [Instalación](#instalación)
  - [Clonar el Repositorio](#clonar-el-repositorio)
  - [Configuración de Variables de Entorno](#configuración-de-variables-de-entorno)
- [Uso](#uso)
  - [Frontend (Página Web)](#frontend-página-web)
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

- @testing-library/jest-dom@5.17.0
- @testing-library/react@13.4.0
- @testing-library/user-event@13.5.0
- @types/jest@27.5.2
- @types/node@16.18.112
- @types/react-dom@18.3.0
- @types/react@18.3.11
- axios@1.7.7
- eslint-config-prettier@9.1.0
- eslint-plugin-react@7.37.1
- eslint@8.57.1
- prettier@3.3.3
- react-dom@18.3.1
- react-router-dom@6.26.2
- react-scripts@5.0.1
- react@18.3.1
- typescript@4.9.5
- web-vitals@2.1.4
- zustand@5.0.0-rc.2


### Backend

- blinker==1.8.2
- click==8.1.7
- Flask==3.0.3
- Flask-SQLAlchemy==3.1.1
- greenlet==3.1.1
- itsdangerous==2.2.0
- Jinja2==3.1.4
- MarkupSafe==3.0.1
- psycopg2==2.9.9
- SQLAlchemy==2.0.35
- typing_extensions==4.12.2
- Werkzeug==3.0.4


### Base de Datos
- **PostgreSQL** ^15.4


### CI/CD
- **GitHub Actions**

## Estructura del Proyecto

```
mi-proyecto/
├── backend/
│   ├── app.py
│   ├── requirements.txt
├── frontend/
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
├── .gitignore
├── README.md
└── LICENSE
```

## Prerequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente en tu máquina:

- [Git](https://git-scm.com/)
- [Node.js](https://nodejs.org/) ^18.0.0
- [Python](https://www.python.org/) ^3.11
- [Yarn](https://yarnpkg.com/) (opcional, si prefieres usar Yarn sobre npm)

## Instalación

### Clonar el Repositorio

```bash
# Clona el repositorio
git clone https://github.com/GeogeYaguana/Papilon.git

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
DATABASE_URL=postgres://ubasg72abi62gl:pe57b2ca8503d9cbd58763ac4a87e1ae4ea39ae84c8ff769f0e87c490647e3472@c9pv5s2sq0i76o.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/ddpb2lu396gu31

# Frontend
REACT_APP_API_URL=http://localhost:5000/

```

**Nota:** Asegúrate de reemplazar `miusuario`, `mipassword` y `mibasededatos` con tus credenciales reales.


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






### Backend (Flask)

El backend proporciona APIs RESTful para interactuar con el frontend y la aplicación móvil.

#### Crear entorno virtual e instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate  # En Linux en windows investigar xd
pip install -r requirements.txt
flask run 

```
pueden probar mediante curl las diferentes peticiones

```bash
curl -X POST http://127.0.0.1:5000/login \
-H "Content-Type: application/json" \
-d '{
    "usuario_nombre": "juanperez",
    "password": "password123"
}'

curl -X GET http://127.0.0.1:5000/usuario

//modificar los parametros este usuario ya fue subido y no acepta usuarios repetidos
curl -X POST http://127.0.0.1:5000/usuario \
-H "Content-Type: application/json" \
-d '{
    "nombre": "Juan Perez",
    "usuario_nombre": "juanperez",
    "password": "password123",
    "correo": "juanperez@gmail.com",
    "tipo_usuario": "local",
    "url_imagen": "https://example.com/imagen.jpg",
    "telefono": "1234567890"
}'



```
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

- **Host:** `c9pv5s2sq0i76o.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com`
- **Puerto:** `5432`
- **Usuario:** `ubasg72abi62gl`
- **Contraseña:** `pe57b2ca8503d9cbd58763ac4a87e1ae4ea39ae84c8ff769f0e87c490647e3472`
- **Base de Datos:** `ddpb2lu396gu31`

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

Si deseas realizar algun cambio sustancial , incrementar alguna funcionalidad , corregir un bug por favor sigue estos pasos para contribuir:

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




# Sistema de Gestión de Cursos

Proyecto web estático para administrar visualmente cursos, estudiantes y
matrículas.

## Estructura del proyecto

```text
Semana13_AlvaroVera/
├── Paginas_Principales/
│   ├── DASHBOARD.html
│   ├── CURSOS.html
│   ├── ESTUDIANTES.html
│   └── MATRICULA.html
├── forms/
│   └── formulario_estudiante.html
├── css/
│   ├── colors.css
│   ├── shared.css
│   ├── animaciones.css
│   ├── dashboard.css
│   ├── formulario_estudiante.css
│   └── matricula.css
└── img/
    ├── cursos_populares.png
    └── matriculas_estado.png
```

## Páginas

- `DASHBOARD.html`: resumen general con tarjetas y gráficos.
- `CURSOS.html`: listado de cursos registrados.
- `ESTUDIANTES.html`: listado de estudiantes y acceso al formulario de alta.
- `MATRICULA.html`: listado de matrículas y filtro de estado.
- `formulario_estudiante.html`: formulario visual para crear estudiantes.

## Estilos

- `colors.css` contiene todas las variables de color del proyecto.
- `shared.css` contiene el reset, la estructura común, navegación, botones,
  controles, tablas y estilos responsive.
- `animaciones.css` contiene las animaciones `@keyframes` (`fadeInUp`, `slideDown`,
  `fadeIn`, `desvanecer`) y las desactiva si el usuario pidió reducir el movimiento.
  Lo cargan las 5 páginas.
- `dashboard.css`, `matricula.css` y `formulario_estudiante.css` contienen solo
  lo específico de su página. Cursos y Estudiantes no necesitan CSS propio.

Las 4 páginas principales usan las mismas clases de estructura:

| Clase            | Elemento                                  |
| ---------------- | ----------------------------------------- |
| `.layout`        | `<body>`: sidebar + contenido             |
| `.sidebar`       | menú lateral (`.sidebar-title`, `.sidebar-nav`, `.sidebar-menu`, `.sidebar-footer`) |
| `.page-main`     | columna de contenido                      |
| `.topbar`        | barra superior                            |
| `.page-content`  | sección con el contenido de la página     |
| `.page-header`   | título, subtítulo y botón de la página    |
| `.page-footer`   | footer inferior                           |
| `.buscador`      | campo de búsqueda                         |
| `.tabla`         | tablas de datos                           |

Las páginas principales incluyen los estilos con rutas relativas:

```html
<link rel="stylesheet" href="../css/colors.css" />
<link rel="stylesheet" href="../css/shared.css" />
```

## Cómo abrir el proyecto

Abre `Paginas_Principales/DASHBOARD.html` en un navegador web. También puedes
usar una extensión como Live Server para facilitar la navegación entre páginas.

## Estado actual

La interfaz y la navegación básica están implementadas. Los datos mostrados
son estáticos; las acciones de crear, editar, eliminar, buscar y filtrar
requieren JavaScript o una conexión con un backend para ser funcionales.

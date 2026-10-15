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
│   ├── dashboard.css
│   ├── cursos.css
│   ├── estudiantes.css
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
- Cada archivo CSS restante contiene los estilos específicos de su página.

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

# Guía de Estructura del Proyecto

## 📁 Organización de Carpetas

```
Semana05_AlvaroVera/
│
├── DASHBOARD.html          # Página principal del dashboard
├── CURSOS.html             # Página de gestión de cursos
├── ESTUDIANTES.html        # Página de gestión de estudiantes
├── MATRICULA.html          # Página de gestión de matrículas
│
└── css/                    # Carpeta de estilos CSS
    ├── shared.css          # Estilos comunes a todas las páginas
    ├── dashboard.css       # Estilos específicos del dashboard
    ├── cursos.css          # Estilos específicos de cursos
    ├── estudiantes.css     # Estilos específicos de estudiantes
    └── matricula.css       # Estilos específicos de matrículas
```

## 🎨 Descripción de los Archivos CSS

### `shared.css` (Estilos Compartidos)

Contiene todos los estilos que se repiten en las 4 páginas:

- Reset de estilos CSS (_margin_, _padding_, _box-sizing_)
- Estilos del body
- Layout principal (flexbox)
- Estilos del header/sidebar
- Estilos de navegación
- Estilos de footer
- Estilos de botones
- Estilos de inputs
- Estilos de tablas
- Estilos de acciones (editar/eliminar)

### `dashboard.css` (Estilos del Dashboard)

Estilos específicos para la página principal:

- Contenido principal
- Header de contenido
- Grid de tarjetas
- Colores de tarjetas (color1 hasta color6)
- Responsive design

### `cursos.css` (Estilos de Cursos)

Estilos específicos para la página de cursos:

- Contenido de la página
- Header de contenido
- Búsqueda

### `estudiantes.css` (Estilos de Estudiantes)

Estilos específicos para la página de estudiantes:

- Contenido de la página
- Header de contenido
- Búsqueda

### `matricula.css` (Estilos de Matrículas)

Estilos específicos para la página de matrículas:

- Contenido de la página
- Header de contenido
- Búsqueda
- Filtro de estado

## ✨ Ventajas de esta Organización

1. **Mantenibilidad**: El código CSS está separado y organizado
2. **Reutilización**: Los estilos comunes están en un archivo central
3. **Escalabilidad**: Fácil agregar nuevas páginas y estilos
4. **Rendimiento**: Los navegadores cachean mejor los archivos CSS
5. **Claridad**: Cada página tiene solo sus estilos específicos
6. **Consistencia**: Todos los estilos comunes están centralizados

## 🚀 Cómo Usar

1. Asegúrate de que la carpeta `css/` esté en la misma carpeta que los archivos HTML
2. Cada archivo HTML importa automáticamente:
   - `css/shared.css` (estilos comunes)
   - `css/[nombre_pagina].css` (estilos específicos)

## 📝 Notas

- Los estilos están bien comentados y organizados
- Se han agregado estilos hover para mejorar la UX
- Incluye media queries responsive (en dashboard.css)
- Todos los colores y dimensiones son consistentes

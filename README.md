# Documentación de Diseño de Ingeniería

En esta sección, se proporciona una visión general del diseño de ingeniería de la aplicación web utilizando el framework Django.

## Introducción al Framework MVC (Model-View-Controller)

Django es un framework de desarrollo web de código abierto basado en el patrón de diseño Modelo-Vista-Controlador (MVC), aunque en Django, el término más utilizado es Modelo-Vista-Plantilla (MVT). 

- **Modelo (Model):** Representa la estructura de datos y la lógica de la aplicación, incluyendo la interacción con la base de datos.
- **Vista (View):** Controla la presentación de la información al usuario y maneja la lógica de la interfaz de usuario.
- **Plantilla (Template):** Define la estructura de las páginas web y cómo se muestran los datos.

Django facilita la separación de preocupaciones al organizar el código de la aplicación en estas tres partes, lo que hace que el desarrollo sea más modular y mantenible.

## Diagrama de Arquitectura del Framework

A continuación, se presenta un diagrama de arquitectura simplificado que representa la estructura de la aplicación web construida con Django:

<p align="center">
  <img src="https://github.com/davidguillen2002/proyectoweb/blob/master/Diagrama%20de%20Arquitectura%20(Django).png" alt="Diagrama de Arquitectura">
</p>

## Explicación del Diagrama

La aplicación web está construida utilizando el framework Django, que sigue el patrón de diseño Modelo-Vista-Plantilla (MVT).

- **Frontend (Cliente):** En el lado del cliente, utilizamos las Plantillas de Django (Templates) para definir la presentación de las páginas web. Estas plantillas se encargan de cómo se mostrarán los datos al usuario y cómo interactuará con la aplicación.

- **Backend (Servidor):** En el lado del servidor, Django se encarga de manejar la lógica de la aplicación. Esto se divide en:

    - **Modelo (Model):** Representa la estructura de datos de la aplicación y define cómo interactuamos con la base de datos. Utilizamos SQLite3 como base de datos para almacenar la información.
    
    - **Lógica de la Aplicación (View):** Aquí se encuentra la lógica de negocio de la aplicación, incluyendo la gestión de las solicitudes del usuario y la respuesta que se envía de vuelta. Django utiliza las Vistas para controlar esto.
    
Este diseño nos permite separar claramente las responsabilidades entre la presentación (Frontend) y la lógica de la aplicación (Backend), lo que facilita el desarrollo, la escalabilidad y el mantenimiento de la aplicación web.

En síntesis, la aplicación web hasta el momento permite a los usuarios realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) a través de una interfaz amigable y segura, gracias a la estructura proporcionada por Django.

# Explicación general del Login:
El sistema de login desarrollado permite a los usuarios registrarse e iniciar sesión de forma segura. Cada usuario solo puede ver y gestionar sus propias tareas, y existe un superusuario con privilegios especiales para administrar usuarios normales.

## Sección Diseño de Ingeniería:

### Diagrama Login:

<p align="center">
  <img src="https://github.com/davidguillen2002/proyectoweb/blob/master/Login.drawio.png" alt="Diagrama de Arquitectura (Login)">
</p>

### Explicación del Diagrama Login:

1. **Página de Login**: Los usuarios llegan a la página de inicio de sesión donde pueden elegir entre registrarse como nuevo usuario o iniciar sesión con sus credenciales existentes.

2. **Registro de Usuario**: Los usuarios nuevos pueden crear una cuenta proporcionando sus datos personales y credenciales.

3. **Iniciar Sesión**: Los usuarios que ya tienen cuentas pueden ingresar sus credenciales para iniciar sesión.

4. **Crear Usuario**: Cuando un usuario se registra, sus datos se almacenan en una base de datos SQLite3, incluyendo credenciales.

5. **Validar Credenciales**: Cuando un usuario inicia sesión, el sistema verifica las credenciales ingresadas.

6. **Almacenar en SQLite3**: Las credenciales y otros datos de usuario se almacenan de manera segura en una base de datos SQLite3 para su posterior validación.

7. **Consultar en la Base de Datos**: Se realiza una consulta a la base de datos SQLite3 para verificar si las credenciales son correctas.
8. **Redirigir a Página de Inicio**: Si las credenciales son correctas, se redirige al usuario a la página de inicio, donde pueden gestionar sus tareas.
9. **Autenticación Exitosa**: Si la autenticación es exitosa, el usuario tiene acceso a su perfil y sus tareas. Si es un superusuario, también tiene acceso a la gestión de usuarios normales.

# Diagrama de Aplicación del Diseño de Ingeniería
## App Web de Gestión Nutricional

<p align="center">
  <img src="https://github.com/davidguillen2002/proyectoweb/blob/master/Diagrama%20de%20App%20Nutricional.png">
</p>

### Descripción
Este diagrama proporciona una vista de alto nivel de cómo se estructura la aplicación. Las clases y paquetes representan distintas responsabilidades y cómo interactúan entre sí. Los detalles específicos de cada clase (como métodos y propiedades) deben ser añadidos según las necesidades específicas de tu proyecto.

### Componentes Principales

#### Usuario
- Registro e inicio de sesión.
- CRUD (Crear, Leer, Actualizar, Eliminar) de alimentos.
- Registro y análisis diario de ingesta nutricional.
- Gestión de perfil nutricional.
- Sugerencias de alimentos basadas en necesidades nutricionales.

#### Base de Datos SQLite3
- Almacena información de usuarios, alimentos, nutrientes, registros diarios y perfiles nutricionales.

#### Vistas (views.py)
- Autenticación de usuarios.
- CRUD de alimentos y nutrientes.
- Listado y gestión de usuarios (para superusuarios).
- Análisis de ingesta nutricional y sugerencias de alimentos.
- Registro y análisis de perfiles nutricionales.

#### Modelos (models.py)
- **Alimento:** Información detallada del alimento.
- **Nutriente:** Información detallada del nutriente.
- **RegistroDiario:** Registro de ingesta diaria del usuario.
- **PerfilNutricional:** Perfil nutricional del usuario.
- **AlimentoNutriente:** Relación entre alimentos y nutrientes.

#### URLs (urls.py)
- Define rutas para las diferentes vistas, incluyendo autenticación, gestión de alimentos y nutrientes, análisis nutricional, etc.

#### Templates
- Interfaces de usuario para todas las funcionalidades, incluyendo registro, inicio de sesión, gestión de alimentos, análisis nutricional, etc.

### Funcionamiento
1. Cálculo de necesidades nutricionales basado en el perfil del usuario.
2. Análisis de ingesta diaria y recomendaciones para cumplir con los objetivos nutricionales.
3. Sugerencias de alimentos ricos en micronutrientes y macronutrientes.
4. La aplicación está desplegada en Render con la URL: [https://nutrivista.onrender.com](https://nutrivista.onrender.com).

### Funcionamiento General
- Los usuarios se registran y acceden a la aplicación.
- Pueden agregar alimentos, registrar su ingesta diaria y recibir análisis y sugerencias nutricionales.
- Los superusuarios gestionan la base de datos de alimentos y nutrientes.
- Se calculan las necesidades nutricionales del usuario basadas en su perfil.
- La aplicación proporciona sugerencias de alimentos para cumplir con las necesidades nutricionales del usuario.

### Sección Diseño de Ingeniería: Funcionamiento del Admin
Esta sección describe cómo funciona la administración del sistema, incluyendo las operaciones CRUD para diferentes entidades como alimentos, nutrientes y usuarios.

#### Funcionalidades del Admin

- **Gestión de Usuarios:** Listar usuarios inactivos, agregar, editar y eliminar usuarios.
- **Gestión de Nutrientes:** Agregar, listar, editar y eliminar nutrientes.
- **Gestión de Alimentos:** Agregar, listar, editar y eliminar alimentos, así como gestionar los nutrientes asociados a los alimentos.

#### Diagrama de Funcionamiento del Admin

<p align="center">
  <img src="https://github.com/davidguillen2002/proyectoweb/blob/master/Diagrama%20Admin%20(Parte%201).png">
</p>

### Sección Diseño de Ingeniería Admin: Validación por Back-End
Esta sección describe cómo el sistema valida las funcionalidades críticas en el back-end, asegurando la integridad y seguridad de los datos. Por ejemplo, la validación del algoritmo se realiza en el controlador en lugar de depender de JavaScript en el cliente.

#### Validaciones Importantes

- **Validación de Acciones de Usuario:** Solo los superusuarios pueden realizar acciones de gestión de nutrientes y alimentos.
- **Validación de Formularios:** Todos los formularios utilizan validación de datos en el servidor para evitar inyecciones de datos maliciosos.
- **Validación de Integridad de Datos:** Antes de eliminar o modificar nutrientes y alimentos, se verifica la existencia de relaciones y dependencias.

#### Diagrama de Validaciones en el Back-End

<p align="center">
  <img src="https://github.com/davidguillen2002/proyectoweb/blob/master/Diagrama%20Admin%20(Parte%202).png">
</p>

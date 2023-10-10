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

### Explicación del diagrama actualizado:

1. **Página de Login**: Los usuarios llegan a la página de inicio de sesión donde pueden elegir entre registrarse como nuevo usuario o iniciar sesión con sus credenciales existentes.

2. **Registro de Usuario**: Los usuarios nuevos pueden crear una cuenta proporcionando sus datos personales y credenciales.

3. **Iniciar Sesión**: Los usuarios que ya tienen cuentas pueden ingresar sus credenciales para iniciar sesión.

4. **Crear Usuario**: Cuando un usuario se registra, sus datos se almacenan en una base de datos SQLite3, incluyendo credenciales.

5. **Validar Credenciales**: Cuando un usuario inicia sesión, el sistema verifica las credenciales ingresadas.

6. **Almacenar en SQLite3**: Las credenciales y otros datos de usuario se almacenan de manera segura en una base de datos SQLite3 para su posterior validación.

7. **Consultar en la Base de Datos**: Se realiza una consulta a la base de datos SQLite3 para verificar si las credenciales son correctas.

8. **Redirigir a Página de Inicio**: Si las credenciales son correctas, se redirige al usuario a la página de inicio, donde pueden gestionar sus tareas.

9. **Autenticación Exitosa**: Si la autenticación es exitosa, el usuario tiene acceso a su perfil y sus tareas. Si es un superusuario, también tiene acceso a la gestión de usuarios normales.


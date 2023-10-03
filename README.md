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

![Diagrama de Arquitectura](https://github.com/davidguillen2002/proyectoweb/blob/master/Diagrama%20de%20Arquitectura%20(Django).png)


## Explicación del Diagrama

La aplicación web está construida utilizando el framework Django, que sigue el patrón de diseño Modelo-Vista-Plantilla (MVT).

- **Frontend (Cliente):** En el lado del cliente, utilizamos las Plantillas de Django (Templates) para definir la presentación de las páginas web. Estas plantillas se encargan de cómo se mostrarán los datos al usuario y cómo interactuará con la aplicación.

- **Backend (Servidor):** En el lado del servidor, Django se encarga de manejar la lógica de la aplicación. Esto se divide en:

    - **Modelo (Model):** Representa la estructura de datos de la aplicación y define cómo interactuamos con la base de datos. Utilizamos SQLite3 como base de datos para almacenar la información.
    
    - **Lógica de la Aplicación (View):** Aquí se encuentra la lógica de negocio de la aplicación, incluyendo la gestión de las solicitudes del usuario y la respuesta que se envía de vuelta. Django utiliza las Vistas para controlar esto.
    
Este diseño nos permite separar claramente las responsabilidades entre la presentación (Frontend) y la lógica de la aplicación (Backend), lo que facilita el desarrollo, la escalabilidad y el mantenimiento de la aplicación web.

En síntesis, la aplicación web hasta el momento permite a los usuarios realizar operaciones CRUD (Crear, Leer, Actualizar y Eliminar) a través de una interfaz amigable y segura, gracias a la estructura proporcionada por Django.



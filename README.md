# Módulo 3 - La HeladerAPI 🍨

## 📖 Descripción

En este proyecto se simula una heladería con autenticación de usuarios y creación de endpoints para la venta de productos y administración de inventario.

Existen 3 tipos de usuarios 🧑‍💼:
- Administrador
- Empleado
- Cliente

La validación de roles se realiza con los campos `is_admin` y `is_employee` en la tabla `users`. Al no ser ni administrador ni empleado, el usuario es de tipo cliente.

Los usuarios iniciales son:
- user: `admin` contraseña: `admin` rol: `is_admin`
- user: `employee` contraseña: `employee` rol: `is_employee`
- user: `client` contraseña: `client`

## 🔗 Endpoints

### Products
- /products/all
    - Muestra todos los productos.
- /products/<int:id>
    - Muestra un producto específico.
- /products/by_name/<name>
    - Muestra un producto por su nombre.
- /sell/<int:id>
    - Vende un producto.
- /products/calculate_calories/<int:id>
    - Calcula las calorías de un producto.
- /products/calculate_cost/<int:id>
    - Calcula el costo de un producto.
- /products/calculate_earnings/<int:id>
    - Calcula las ganancias de un producto.

### Ingredients
- /ingredients/all
    - Muestra todos los ingredientes.
- /ingredients/<int:id>
    - Muestra un ingrediente específico.
- /ingredients/by_name/<name>
    - Muestra un ingrediente por su nombre.
- /stock/<int:id>
    - Aumenta el stock de un ingrediente.
- /renew/<int:id>
    - Restablece el stock de un ingrediente.
- /ingredients/<int:id>/is_healthy
    - Muestra si un ingrediente es saludable.

## 💾 Base de datos

Para restaurar la base de datos, se debe comentar la línea 30 en `app.py`, ejecutar la función `init_db()`.
También hay una copia de la base de datos en el archivo `Dump.sql` en la carpeta `database`.

## 📊 Diagrama Entidad Relación

![Diagrama Entidad Relación](./Diagrama%20Entidad%20Relaci%C3%B3n.png)
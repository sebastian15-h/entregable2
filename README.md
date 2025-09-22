1. Instalar dependencias


text
tkinter
mysql-connector-python
reportlab
tkcalendar
customtkinter
CTkMessagebox
pillow
pandas
Luego instálalas:

bash
pip install -r requirements.txt
2. Preparar la base de datos
Asegúrate de tener MySQL ejecutándose

Crea una base de datos llamada hoteel

El usuario debe ser root sin contraseña (o modifica las credenciales en el código)

3. Ejecutar la aplicación
bash
python main.py
4. Estructura de archivos necesaria
Asegúrate de tener estos archivos en la misma carpeta:

main.py (tu código principal)

favicon.ico (icono de la ventana)

guardar.png, actualizar.png, borrar.png, limpiar.png, buscar.png (iconos de botones)

Carpeta imagenes_empleados/ (se crea automáticamente)

5. Problemas comunes
Si hay errores de importación:

bash
# Si customtkinter no se instala correctamente:
pip install customtkinter --upgrade

# Si tkcalendar da problemas:
pip install tkcalendar
La aplicación debería iniciar mostrando una interfaz con 4 pestañas para gestionar hoteles, clientes, empleados y temporadas.

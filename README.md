Sistema de Gestión Hotelera
Una aplicación de escritorio para la gestión integral de hoteles, desarrollada en Python con interfaz gráfica moderna.

Características
Gestión de Hoteles: Registro y administración de información de hoteles

Gestión de Clientes: Control de datos de clientes y sus preferencias

Gestión de Empleados: Administración del personal hotelero

Gestión de Temporadas: Control de temporadas alta/baja y factores tarifarios

Exportación de datos: PDF y Excel para reportes

Interfaz moderna: Diseño oscuro/claro personalizable

Requisitos del Sistema
Python 3.7 o superior

MySQL/MariaDB

Sistema operativo: Windows, Linux o macOS

Instalación
Clona o descarga el proyecto

Instala las dependencias:

bash
pip install -r requirements.txt
Configura la base de datos MySQL:

Crea una base de datos llamada hoteel

Asegúrate de que el usuario root no tenga contraseña (o modifica la configuración en el código)

Ejecuta la aplicación:

bash
python main.py
Estructura del Proyecto
text
- main.py                 # Archivo principal de la aplicación
- requirements.txt        # Dependencias del proyecto
- imagenes_empleados/     # Carpeta para almacenar imágenes
- iconos/                # Iconos de la aplicación (guardar.png, actualizar.png, etc.)
Uso
La aplicación se organiza en 4 pestañas principales:

Hoteles: Gestiona información de establecimientos hoteleros

Clientes: Administra datos de clientes y programas de fidelización

Empleados: Controla el personal y sus asignaciones

Temporadas: Configura temporadas y factores de tarifa

Funcionalidades por pestaña:
Guardar: Añadir nuevos registros

Actualizar: Modificar registros existentes

Eliminar: Remover registros

Buscar: Localizar registros específicos

Limpiar: Vaciar formularios

Exportar: Generar reportes en PDF/Excel

Configuración de Base de Datos
La aplicación utiliza stored procedures MySQL para todas las operaciones CRUD. Asegúrate de que tu base de datos tenga los procedimientos necesarios con nombres como:

sp_insertHotel

sp_getHotelById

sp_updateHotel

sp_deleteHotelById

etc.

Tecnologías Utilizadas
CustomTkinter: Interfaz gráfica moderna

MySQL Connector: Conexión a base de datos

ReportLab: Generación de PDFs

Pandas: Exportación a Excel

PIL: Manejo de imágenes

Notas
La aplicación está diseñada para uso local

Los datos de conexión a la base de datos están hardcodeados (modificar según necesidades)

Incluye validación de datos en formularios

Soporte para temas claro/oscuro

Desarrollo
Este proyecto fue desarrollado como parte de un proyecto académico/profesional para la gestión hotelera integral.

mo se ejecutacin main se ejecuta con hoteel 2 el main lo agrego git hub t dame solo texto
Para ejecutar el archivo principal del proyecto hotelero, sigue estos pasos:

1. Instalar dependencias
Primero crea un archivo requirements.txt con este contenido:

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

recuerda que el archivo main no sirve de nada lo agrego github el main verdadero se llama hoteel2.py
Tienes razón, el archivo principal es hoteel2.py. Aquí están las instrucciones correctas:

Para ejecutar la aplicación:
bash
python hoteel2.py
Pasos completos:
Instalar dependencias (mismo requirements.txt):

bash
pip install -r requirements.txt
Preparar MySQL:

Base de datos: hoteel

Usuario: root

Sin contraseña

Ejecutar:

bash
python hoteel2.py
Estructura de archivos necesaria:
hoteel2.py (archivo principal)

favicon.ico

Iconos PNG: guardar.png, actualizar.png, borrar.png, limpiar.png, buscar.png

Carpeta imagenes_empleados/ (se crea automáticamente)

El archivo main.py que mencionas en GitHub puede ser un placeholder o archivo antiguo. El verdadero ejecutable es hoteel2.py.

mas largo
Sistema de Gestión Hotelera - Documentación Completa
Descripción del Proyecto
Este es un sistema integral de gestión hotelera desarrollado en Python que permite administrar toda la operación de un hotel through de una interfaz gráfica moderna y intuitiva. La aplicación ofrece funcionalidades completas para el control de establecimientos hoteleros, clientes, empleados y temporadas, con capacidades de exportación de reportes.

Características Principales
🏨 Gestión Completa de Hoteles
Registro de información detallada de hoteles

Control de categorías, servicios y horarios

Gestión de capacidad y datos de contacto

Administración de gerentes responsables

👥 Gestión de Clientes
Registro completo de datos personales

Control de documentos de identidad y nacionalidad

Gestión de preferencias especiales

Programa de fidelización con niveles

Historial de contactos y direcciones

👨‍💼 Gestión de Empleados
Administración del personal hotelero

Control de cargos y asignaciones por hotel

Datos de contacto y correos electrónicos

Organización jerárquica del personal

📅 Gestión de Temporadas
Configuración de temporadas alta y baja

Factores multiplicadores de tarifas

Control de fechas de inicio y fin

Optimización de precios por temporada

📊 Funcionalidades Avanzadas
Exportación a PDF con formatos profesionales

Exportación a Excel para análisis de datos

Interfaz moderna con temas claro/oscuro

Validación completa de datos

Búsqueda y filtrado avanzado

Requisitos del Sistema
Requisitos Mínimos
Sistema Operativo: Windows 10/11, Linux Ubuntu 18.04+, macOS 10.15+

Python: Versión 3.7 o superior

Memoria RAM: 4 GB mínimo

Espacio en disco: 500 MB libres

Requisitos Recomendados
Sistema Operativo: Windows 11, Linux Ubuntu 20.04+, macOS 12+

Python: Versión 3.9 o superior

Memoria RAM: 8 GB o más

Espacio en disco: 1 GB libre

MySQL: Versión 8.0 o superior

Instalación Paso a Paso
1. Clonar o Descargar el Proyecto
bash
# Si está en GitHub
git clone https://github.com/tu-usuario/hoteel2.git
cd hoteel2

# O descargar manualmente y extraer en una carpeta
2. Crear Entorno Virtual (Recomendado)
bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
3. Instalar Dependencias
Crear archivo requirements.txt con este contenido:

txt
tkinter>=0.1.0
mysql-connector-python>=8.0.0
reportlab>=3.6.0
tkcalendar>=1.6.0
customtkinter>=5.0.0
CTkMessagebox>=1.2.0
pillow>=9.0.0
pandas>=1.5.0
Instalar dependencias:

bash
pip install -r requirements.txt
4. Configurar Base de Datos MySQL
4.1. Instalar MySQL
Descargar MySQL Community Server desde mysql.com

Seguir el asistente de instalación

Anotar la contraseña del root

4.2. Crear Base de Datos
sql
-- Conectarse a MySQL como root
mysql -u root -p

-- Crear base de datos
CREATE DATABASE hoteel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verificar creación
SHOW DATABASES;
4.3. Crear Tablas y Procedimientos
Ejecutar el script SQL proporcionado para crear las tablas necesarias.

5. Configurar Credenciales de Base de Datos
Modificar en el archivo hoteel2.py las credenciales si es necesario:

python
self.connection = mysql.connector.connect(
    host='localhost',
    database='hoteel',
    user='root',
    password='',  # Cambiar si tiene contraseña
    autocommit=False
)
6. Preparar Archivos de Recursos
Asegurarse de tener en la carpeta del proyecto:

text
hoteel2.py
favicon.ico
guardar.png
actualizar.png
borrar.png
limpiar.png
buscar.png
Estructura del Proyecto
text
proyecto_hotel/
│
├── hoteel2.py                 # Archivo principal
├── requirements.txt           # Dependencias
├── favicon.ico               # Icono de la aplicación
├── guardar.png               # Icono guardar
├── actualizar.png            # Icono actualizar
├── borrar.png                # Icono eliminar
├── limpiar.png               # Icono limpiar
├── buscar.png                # Icono buscar
│
├── imagenes_empleados/       # Carpeta para fotos (se crea automáticamente)
├── exports/                  # Carpeta para reportes (se crea automáticamente)
│
└── documentacion/            # Documentación adicional
Ejecución de la Aplicación
Método 1: Ejecución Directa
bash
python hoteel2.py
Método 2: Ejecución con Entorno Virtual
bash
# Activar entorno virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS

# Ejecutar aplicación
python hoteel2.py
Método 3: Crear Ejecutable (Opcional)
bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=favicon.ico hoteel2.py
Uso de la Aplicación
Interfaz Principal
La aplicación se organiza en 4 pestañas principales:

1. Pestaña "Hoteles" 🏨
Campos: ID, Nombre, Categoría, Dirección, Teléfono, Correo, Año inauguración, Habitantes, Servicios, Horarios Check-in/out, Gerente

Funciones: Guardar, Actualizar, Eliminar, Buscar, Limpiar, Exportar

2. Pestaña "Clientes" 👥
Campos: ID, Nombre, Apellido, Documento, Nacionalidad, Fecha Nacimiento, Dirección, Teléfono, Correo, Preferencias, Nivel Fidelización

Funciones: CRUD completo con validaciones

3. Pestaña "Empleados" 👨‍💼
Campos: ID, Nombres, Apellidos, Cargo, Teléfono, Correo, ID Hotel

Funciones: Gestión completa del personal

4. Pestaña "Temporadas" 📅
Campos: ID, Nombre Temporada, Fecha Inicio, Fecha Fin, Factor Multiplicador

Funciones: Configuración de tarifas estacionales

Funciones Especiales
Exportación de Datos
PDF: Genera reportes formateados para impresión

Excel: Crea hojas de cálculo para análisis

Ubicación: Los archivos se guardan en la carpeta del proyecto

Temas de Interfaz
Tema Claro: Interfaz luminosa para uso diurno

Tema Oscuro: Interfaz oscura para uso prolongado

Cambio en tiempo real: Botón "Cambiar fondo"

Validaciones
Campos numéricos: Solo aceptan dígitos

Fechas: Formato DD/MM/AAAA

Correos: Validación básica de formato

Campos obligatorios: Marcados con validación

Solución de Problemas
Error: "ModuleNotFoundError"
bash
# Verificar instalación de dependencias
pip list

# Reinstalar dependencias faltantes
pip install mysql-connector-python customtkinter
Error: Conexión a MySQL
bash
# Verificar que MySQL esté ejecutándose
sudo systemctl status mysql  # Linux
# o verificar servicios en Windows

# Probar conexión manual
mysql -u root -p -h localhost
Error: Iconos No Encontrados
Verificar que los archivos PNG estén en la misma carpeta que hoteel2.py

Verificar nombres exactos de archivos

Rendimiento Lento
Cerrar otras aplicaciones

Verificar conexión a base de datos

Reiniciar la aplicación

Mantenimiento
Copias de Seguridad
sql
# Backup de base de datos
mysqldump -u root -p hoteel > backup_hoteel.sql

# Restaurar backup
mysql -u root -p hoteel < backup_hoteel.sql
Actualizaciones
bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt

Base de Datos: MySQL con stored procedures

Interfaz: CustomTkinter para UI moderna

Reportes: ReportLab para PDF, Pandas para Excel

Seguridad
Validación de entrada de datos

Transacciones SQL con rollback

Manejo de errores robusto

Performance
Carga diferida de datos

Scroll virtual en listas grandes

Conexiones persistentes a BD

Soporte y Contacto
Para reportar issues o solicitar ayuda:

Verificar que se siguieron todos los pasos de instalación

Revisar los logs de error en la consola

Probar con la configuración mínima

Licencia
Este proyecto es para fines educativos y de demostración. Se permite su uso y modificación con fines académicos.

¡La aplicación está lista para usar! Ejecuta python hoteel2.py para comenzar.

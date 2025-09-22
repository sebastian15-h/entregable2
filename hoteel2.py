import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Table
from reportlab.lib.pagesizes import A4, landscape
from tkcalendar import DateEntry
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from tkinter import filedialog
from PIL import Image
from customtkinter import CTkImage
from reportlab.pdfgen import canvas
from PIL import Image, ImageTk
import pandas as pd
from reportlab.lib.pagesizes import letter
import os



# =================== CONFIGURACIÓN DE BASE DE DATOS ===================
class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='hoteel',
                user='root',
                password='',
                autocommit=False
            )
            self.cursor = self.connection.cursor(buffered=True)
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"Error conectando a la base de datos: {err}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def call_procedure(self, procedure_name, parameters=None):
        try:
            if parameters:
                self.cursor.callproc(procedure_name, parameters)
            else:
                self.cursor.callproc(procedure_name)

            # Obtener resultados
            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())

            return True, results
        except mysql.connector.Error as err:
            self.connection.rollback()
            return False, str(err)


# Instancia global de conexión
db = DatabaseConnection()

import mysql.connector

def cargar_datos_hoteles():
    # Limpiar el Treeview para no duplicar datos
    for item in hoteles_tree.get_children():
        hoteles_tree.delete(item)

    # Conectar a la base de datos (ajusta con tus datos)
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='hoteel'
    )
    cursor = conexion.cursor()

    # Ejecutar consulta para obtener fincas
    consulta = """
        SELECT id_hotel, nombre_hotel, categoria, direccion, telefono,
               correo, año_inauguracion, numero_total_habitantes, servicios_disponibles, horarios_check_in, horarios_check_out, gerente_responsable 
        FROM hoteles
    """
    cursor.execute(consulta)
    filas = cursor.fetchall()

    # Insertar filas en el Treeview
    for fila in filas:
        hoteles_tree .insert('', 'end', values=fila)

    cursor.close()
    conexion.close()

def cargar_datos_clientes():
    # Limpiar el Treeview para no duplicar datos
    for item in clientes_tree.get_children():
        clientes_tree.delete(item)

    # Conectar a la base de datos (ajusta con tus datos)
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='hoteel'
    )
    cursor = conexion.cursor()

    # Ejecutar consulta para obtener fincas
    consulta = """
        SELECT id_cliente, nombre, apellido, documento_identidad, nacionalidad, fecha_nacimiento, direccion, telefono, correo, preferencias_especiales, nivel_programa_fidelizacion
        FROM clientes
    """
    cursor.execute(consulta)
    filas = cursor.fetchall()

    # Insertar filas en el Treeview
    for fila in filas:
        clientes_tree.insert('', 'end', values=fila)

    cursor.close()
    conexion.close()

def cargar_datos_empleados():
    # Limpiar el Treeview para no duplicar datos
    for item in empleados_tree.get_children():
        empleados_tree.delete(item)

    # Conectar a la base de datos (ajusta con tus datos)
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='hoteel'
    )
    cursor = conexion.cursor()

    # Ejecutar consulta para obtener empleados
    consulta = """
        SELECT id_empleado, nombres, apellidos, cargo, telefono, correo, id_hotel
        FROM empleados
    """
    cursor.execute(consulta)
    filas = cursor.fetchall()

    # Insertar filas en el Treeview
    for fila in filas:
        empleados_tree.insert('', 'end', values=fila)

    cursor.close()
    conexion.close()


def cargar_datos_temporadas():
    # Limpiar el Treeview para no duplicar datos
    for item in temporadas_tree.get_children():
        temporadas_tree.delete(item)

    # Conectar a la base de datos (ajusta con tus datos)
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='hoteel'
    )
    cursor = conexion.cursor()

    # Ejecutar consulta para obtener temporadas
    consulta = """
        SELECT id_temporada, nombre_temporada, fecha_inicio, fecha_fin, factor_multiplicador_tarifa
        FROM temporadas
    """
    cursor.execute(consulta)
    filas = cursor.fetchall()

    # Insertar filas en el Treeview
    for fila in filas:
        temporadas_tree.insert('', 'end', values=fila)

    cursor.close()
    conexion.close()






# =================== FUNCIONES DE VALIDACIÓN ===================
def validate_numeric(value, field_name, force_int=False):
    if not value.strip():
        return False, None  # ID NO puede estar vacío

    try:
        val = int(value) if force_int else (float(value) if '.' in value else int(value))
        return True, val
    except ValueError:
        messagebox.showerror("Error de Validación", f"{field_name} debe ser un número válido")
        return False, None




def validate_required(value, field_name):
    if not value.strip():
        CTkMessagebox(title="Error de Validación", message=f"{field_name} es requerido")
        return False
    return True


def validate_date(date_string):
    if not date_string.strip():
        return True, None
    try:
        # Aceptar formato YYYY-MM-DD
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        return True, date_obj
    except ValueError:
        messagebox.showerror("Error de Validación", "Fecha debe estar en formato YYYY-MM-DD")
        return False, None


# =================== FUNCIONES PARA HOTELES ===================
import datetime


def guardar_hotel():
    # Obtener valores de los Entry
    try:
        id_val = int(idhotel.get())
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    nombre_val = nombre_hotel.get().strip()
    categoria_val = categoria.get().strip()
    direccion_val = direccion.get().strip()
    telefono_val = tel.get().strip()
    correo_val = correo.get().strip()
    año_inauguracion_val = año_inauguracion.get().strip()
    habitantes_val = habitantes.get().strip()
    servicios_val = servicios.get().strip()
    checkin_val = checkin.get().strip()
    checkout_val = checkout.get().strip()
    gerente_val = gerente.get().strip()

    # Validaciones básicas
    if not nombre_val or not direccion_val:
        messagebox.showerror("Error", "Nombre y Dirección son campos obligatorios.")
        return

    # Convertir campos numéricos y fechas/hora adecuadamente
    try:
        categoria_val_int = int(categoria_val) if categoria_val else None
    except ValueError:
        messagebox.showerror("Error", "Categoría debe ser un número entero.")
        return

    try:
        telefono_val_int = int(telefono_val) if telefono_val else None
    except ValueError:
        messagebox.showerror("Error", "Teléfono debe ser un número entero.")
        return

    try:
        año_inauguracion_val_dec = int(año_inauguracion_val) if año_inauguracion_val else None
    except ValueError:
        messagebox.showerror("Error", "Año de inauguración debe ser un número entero.")
        return

    try:
        habitantes_val_int = int(habitantes_val) if habitantes_val else None
    except ValueError:
        messagebox.showerror("Error", "Habitantes debe ser un número entero.")
        return

    # Convertir horarios a formato HH:MM:SS o None
    from datetime import datetime

    def parse_time(t):
        try:
            return datetime.strptime(t, "%H:%M:%S").time()
        except Exception:
            return None

    checkin_val_time = parse_time(checkin_val)
    checkout_val_time = parse_time(checkout_val)

    # Llamar procedimiento almacenado
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            "CALL sp_insertHotel(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                id_val,
                nombre_val,
                categoria_val_int,
                direccion_val,
                telefono_val_int,
                correo_val,
                año_inauguracion_val_dec,
                habitantes_val_int,
                servicios_val,
                checkin_val_time,
                checkout_val_time,
                gerente_val,
            ),
        )
        db.connection.commit()
        messagebox.showinfo("Éxito", "Hotel guardado correctamente.")
        cargar_datos_hoteles()
        limpiar_campos_hoteles()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el hotel: {e}")
    finally:
        cursor.close()



def buscar_hotel_por_id():
    id_val = idhotel.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID del hotel para buscar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    success, result = db.call_procedure('sp_getHotelById', (id_val_int,))

    if not success:
        messagebox.showerror("Error", f"Error al buscar el hotel: {result}")
        return

    # result es lista de filas, obtenemos la primera si existe
    if result and len(result) > 0:
        fila = result[0]

        idhotel.delete(0, "end")
        idhotel.insert(0, fila[0])

        nombre_hotel.delete(0, "end")
        nombre_hotel.insert(0, fila[1])

        categoria.delete(0, "end")
        categoria.insert(0, fila[2] if fila[2] is not None else '')

        direccion.delete(0, "end")
        direccion.insert(0, fila[3])

        tel.delete(0, "end")
        tel.insert(0, fila[4] if fila[4] is not None else '')

        correo.delete(0, "end")
        correo.insert(0, fila[5] if fila[5] is not None else '')

        año_inauguracion.delete(0, "end")
        año_inauguracion.insert(0, fila[6] if fila[6] is not None else '')

        habitantes.delete(0, "end")
        habitantes.insert(0, fila[7] if fila[7] is not None else '')

        servicios.delete(0, "end")
        servicios.insert(0, fila[8] if fila[8] is not None else '')

        checkin.delete(0, "end")
        checkin.insert(0, str(fila[9]) if fila[9] is not None else '')

        checkout.delete(0, "end")
        checkout.insert(0, str(fila[10]) if fila[10] is not None else '')

        gerente.delete(0, "end")
        gerente.insert(0, fila[11] if fila[11] is not None else '')

        messagebox.showinfo("Éxito", "Hotel encontrado y datos cargados.")
    else:
        messagebox.showinfo("No encontrado", f"No se encontró ningún hotel con ID {id_val_int}.")


def limpiar_campos_hoteles():
    idhotel.delete(0, "end")
    nombre_hotel.delete(0, "end")
    categoria.delete(0, "end")
    direccion.delete(0, "end")
    tel.delete(0, "end")
    correo.delete(0, "end")
    año_inauguracion.delete(0, "end")
    habitantes.delete(0, "end")
    servicios.delete(0, "end")
    checkin.delete(0, "end")
    checkout.delete(0, "end")
    gerente.delete(0, "end")

def eliminar_hotel():
    id_val = idhotel.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID del hotel para eliminar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro que desea eliminar el hotel con ID {id_val_int}?")
    if not respuesta:
        return

    cursor = db.connection.cursor()
    try:
        cursor.execute("CALL sp_deleteHotelById(%s)", (id_val_int,))
        db.connection.commit()  # <--- Este es el commit para guardar los cambios
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Hotel eliminado correctamente.")
            limpiar_campos_hoteles()
            cargar_datos_hoteles()
        else:
            messagebox.showwarning("Atención", "No se encontró hotel con ese ID.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el hotel: {e}")
    finally:
        cursor.close()

def actualizar_hotel():
    # Obtener valores de los Entry
    try:
        id_val = int(idhotel.get())
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    nombre_val = nombre_hotel.get().strip()
    categoria_val = categoria.get().strip()
    direccion_val = direccion.get().strip()
    telefono_val = tel.get().strip()
    correo_val = correo.get().strip()
    año_inauguracion_val = año_inauguracion.get().strip()
    habitantes_val = habitantes.get().strip()
    servicios_val = servicios.get().strip()
    checkin_val = checkin.get().strip()
    checkout_val = checkout.get().strip()
    gerente_val = gerente.get().strip()

    # Validaciones básicas
    if not nombre_val or not direccion_val:
        messagebox.showerror("Error", "Nombre y Dirección son campos obligatorios.")
        return

    # Convertir campos numéricos y fechas/hora adecuadamente
    try:
        categoria_val_int = int(categoria_val) if categoria_val else None
    except ValueError:
        messagebox.showerror("Error", "Categoría debe ser un número entero.")
        return

    try:
        telefono_val_int = int(telefono_val) if telefono_val else None
    except ValueError:
        messagebox.showerror("Error", "Teléfono debe ser un número entero.")
        return

    try:
        año_inauguracion_val_dec = int(año_inauguracion_val) if año_inauguracion_val else None
    except ValueError:
        messagebox.showerror("Error", "Año de inauguración debe ser un número entero.")
        return

    try:
        habitantes_val_int = int(habitantes_val) if habitantes_val else None
    except ValueError:
        messagebox.showerror("Error", "Habitantes debe ser un número entero.")
        return

    # Convertir horarios a formato HH:MM:SS o None
    from datetime import datetime

    def parse_time(t):
        try:
            return datetime.strptime(t, "%H:%M:%S").time()
        except Exception:
            return None

    checkin_val_time = parse_time(checkin_val)
    checkout_val_time = parse_time(checkout_val)

    # Llamar procedimiento almacenado
    cursor = db.connection.cursor()
    try:
        cursor.execute(
            "CALL sp_updateHotel(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (
                id_val,
                nombre_val,
                categoria_val_int,
                direccion_val,
                telefono_val_int,
                correo_val,
                año_inauguracion_val_dec,
                habitantes_val_int,
                servicios_val,
                checkin_val_time,
                checkout_val_time,
                gerente_val,
            ),
        )
        db.connection.commit()
        messagebox.showinfo("Éxito", "Hotel actualizado correctamente.")
        cargar_datos_hoteles()
        limpiar_campos_hoteles()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el hotel: {e}")
    finally:
        cursor.close()





# =================== FUNCIONES PARA CLIENTES ===================


def buscar_cliente():
    id_val = id_cliente.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID del cliente para buscar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    success, result = db.call_procedure('sp_buscar_cliente', (id_val_int,))

    if not success:
        messagebox.showerror("Error", f"Error al buscar el cliente: {result}")
        return

    if result and len(result) > 0:
        fila = result[0]

        id_cliente.delete(0, "end")
        id_cliente.insert(0, fila[0])

        nombre.delete(0, "end")
        nombre.insert(0, fila[1])

        apellido.delete(0, "end")
        apellido.insert(0, fila[2])

        documento_identidad.delete(0, "end")
        documento_identidad.insert(0, fila[3])

        nacionalidad.delete(0, "end")
        nacionalidad.insert(0, fila[4] if fila[4] is not None else '')

        fecha_nacimiento.delete(0, "end")
        fecha_nacimiento.insert(0, str(fila[5]) if fila[5] is not None else '')

        direccion_clientes.delete(0, "end")
        direccion_clientes.insert(0, fila[6] if fila[6] is not None else '')

        telefono.delete(0, "end")
        telefono.insert(0, fila[7] if fila[7] is not None else '')

        correo.delete(0, "end")
        correo.insert(0, fila[8] if fila[8] is not None else '')

        preferencias_especiales.delete(0, "end")
        preferencias_especiales.insert(0, fila[9] if fila[9] is not None else '')

        nivel_programa_fidelizacion.delete(0, "end")
        nivel_programa_fidelizacion.insert(0, fila[10] if fila[10] is not None else '')

        messagebox.showinfo("Éxito", "Cliente encontrado y datos cargados.")
    else:
        messagebox.showinfo("No encontrado", f"No se encontró ningún cliente con ID {id_val_int}.")

def limpiar_campos_cliente():
    id_cliente.delete(0, "end")
    nombre.delete(0, "end")
    apellido.delete(0, "end")
    documento_identidad.delete(0, "end")
    nacionalidad.delete(0, "end")
    fecha_nacimiento.delete(0, "end")
    direccion_clientes.delete(0, "end")
    telefono.delete(0, "end")
    correo.delete(0, "end")
    preferencias_especiales.delete(0, "end")
    nivel_programa_fidelizacion.delete(0, "end")


def eliminar_cliente():
    id_val = id_cliente.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID del cliente para eliminar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro que desea eliminar el cliente con ID {id_val_int}?")
    if not respuesta:
        return

    cursor = db.connection.cursor()
    try:
        cursor.execute("CALL sp_eliminar_cliente(%s)", (id_val_int,))
        db.connection.commit()  # <--- Commit para guardar los cambios
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Cliente eliminado correctamente.")
            limpiar_campos_cliente()
            cargar_datos_clientes()
        else:
            messagebox.showwarning("Atención", "No se encontró cliente con ese ID.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el cliente: {e}")
    finally:
        cursor.close()

def actualizar_cliente():
    id_val = id_cliente.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID del cliente para actualizar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    # Recoger los datos de los entrys
    nombre_val = nombre.get().strip()
    apellido_val = apellido.get().strip()
    documento_val = documento_identidad.get().strip()
    nacionalidad_val = nacionalidad.get().strip()
    fecha_nac_val = fecha_nacimiento.get().strip()
    direccion_val = direccion_clientes.get().strip()
    telefono_val = telefono.get().strip()
    correo_val = correo.get().strip()
    pref_esp_val = preferencias_especiales.get().strip()
    nivel_fidel_val = nivel_programa_fidelizacion.get().strip()

    # Validaciones mínimas
    if not nombre_val or not apellido_val or not documento_val:
        messagebox.showerror("Error", "Nombre, apellido y documento de identidad son obligatorios.")
        return

    try:
        documento_val_int = int(documento_val)
    except ValueError:
        messagebox.showerror("Error", "Documento de identidad debe ser un número entero.")
        return

    try:
        if telefono_val:
            telefono_val_int = int(telefono_val)
        else:
            telefono_val_int = None
    except ValueError:
        messagebox.showerror("Error", "Teléfono debe ser un número entero.")
        return

    # Opcional: Validar fecha con formato YYYY-MM-DD si quieres

    cursor = db.connection.cursor()
    try:
        cursor.execute(
            "CALL sp_actualizar_cliente(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                id_val_int,
                nombre_val,
                apellido_val,
                documento_val_int,
                nacionalidad_val if nacionalidad_val else None,
                fecha_nac_val if fecha_nac_val else None,
                direccion_val if direccion_val else None,
                telefono_val_int,
                correo_val if correo_val else None,
                pref_esp_val if pref_esp_val else None,
                nivel_fidel_val if nivel_fidel_val else None,
            )
        )
        db.connection.commit()
        messagebox.showinfo("Éxito", "Cliente actualizado correctamente.")
        cargar_datos_clientes()
        limpiar_campos_cliente()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el cliente: {e}")
    finally:
        cursor.close()

def guardar_cliente():
    try:
        cursor = db.connection.cursor()
        cursor.execute("CALL sp_insertar_cliente(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
            nombre.get(),
            apellido.get(),
            int(documento_identidad.get()),
            nacionalidad.get(),
            fecha_nacimiento.get(),  # Asegúrate de enviar en formato 'YYYY-MM-DD'
            direccion_clientes.get(),
            int(telefono.get()) if telefono.get() else None,
            correo.get(),
            preferencias_especiales.get(),
            nivel_programa_fidelizacion.get()
        ))
        db.connection.commit()
        messagebox.showinfo("Éxito", "Cliente guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el cliente: {e}")

def actualizar_empleado():
    id_val = id_empleado.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID del empleado para actualizar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    # Obtener los datos de los campos
    nombres_val = nombres.get().strip()
    apellidos_val = apellidos.get().strip()
    cargo_val = cargo.get().strip()
    telefono_val = telefono.get().strip()
    correo_val = correo.get().strip()

    id_hotel_val = id_hotel.get().strip()
    try:
        id_hotel_int = int(id_hotel_val) if id_hotel_val else None
    except ValueError:
        messagebox.showerror("Error", "El ID del hotel debe ser un número entero.")
        return

    # Validar campos obligatorios
    if not nombres_val or not apellidos_val or not cargo_val:
        messagebox.showerror("Error", "Por favor complete los campos obligatorios: nombres, apellidos y cargo.")
        return

    cursor = db.connection.cursor()
    try:
        cursor.callproc('sp_updateEmpleado', (
            id_val_int,
            nombres_val,
            apellidos_val,
            cargo_val,
            telefono_val,
            correo_val,
            id_hotel_int
        ))
        db.connection.commit()
        messagebox.showinfo("Éxito", "Empleado actualizado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar el empleado: {e}")
    finally:
        cursor.close()




# =================== FUNCIONES PARA EMPLEADOS ===================

def guardar_empleado():
    id_val = id_empleado.get()
    nom = nombres.get()
    ape = apellidos.get()
    car = cargo.get()
    tel = telefono.get()
    mail = correo.get()
    id_h = id_hotel.get()

    # Validaciones básicas
    if not id_val.strip() or not nom.strip() or not ape.strip():
        messagebox.showerror("Error", "Por favor complete los campos obligatorios: ID, nombres y apellidos.")
        return

    try:
        id_val_int = int(id_val)
        id_h_int = int(id_h) if id_h.strip() else None
    except ValueError:
        messagebox.showerror("Error", "El ID y el ID de hotel deben ser números enteros.")
        return

    cursor = db.connection.cursor()
    try:
        cursor.execute("CALL sp_guardarEmpleado(%s, %s, %s, %s, %s, %s, %s)",
                       (id_val_int, nom, ape, car, tel, mail, id_h_int))
        db.connection.commit()
        messagebox.showinfo("Éxito", "Empleado guardado correctamente.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el empleado: {e}")
    finally:
        cursor.close()

def buscar_empleado():
    id_val = id_empleado.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID del empleado para buscar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    success, result = db.call_procedure('sp_buscarEmpleado', (id_val_int,))

    if not success:
        messagebox.showerror("Error", f"Error al buscar el empleado: {result}")
        return

    if result and len(result) > 0:
        fila = result[0]

        id_empleado.delete(0, "end")
        id_empleado.insert(0, fila[0])

        nombres.delete(0, "end")
        nombres.insert(0, fila[1])

        apellidos.delete(0, "end")
        apellidos.insert(0, fila[2])

        cargo.delete(0, "end")
        cargo.insert(0, fila[3] if fila[3] is not None else '')

        telefono.delete(0, "end")
        telefono.insert(0, fila[4] if fila[4] is not None else '')

        correo.delete(0, "end")
        correo.insert(0, fila[5] if fila[5] is not None else '')

        id_hotel.delete(0, "end")
        id_hotel.insert(0, fila[6] if fila[6] is not None else '')

        messagebox.showinfo("Éxito", "Empleado encontrado y datos cargados.")
    else:
        messagebox.showinfo("No encontrado", f"No se encontró ningún empleado con ID {id_val_int}.")

def limpiar_empleado():
    id_empleado.delete(0, "end")
    nombres.delete(0, "end")
    apellidos.delete(0, "end")
    cargo.delete(0, "end")
    telefono.delete(0, "end")
    correo.delete(0, "end")
    id_hotel.delete(0, "end")

def eliminar_empleado():
    id_val = id_empleado.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID del empleado para eliminar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    respuesta = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro que desea eliminar al empleado con ID {id_val_int}?")
    if not respuesta:
        return

    cursor = db.connection.cursor()
    try:
        cursor.execute("CALL sp_deleteEmpleadoById(%s)", (id_val_int,))
        db.connection.commit()
        if cursor.rowcount > 0:
            messagebox.showinfo("Éxito", "Empleado eliminado correctamente.")
            limpiar_empleado()
            cargar_datos_empleados()  # Asegúrate que esta función exista para refrescar la lista
        else:
            messagebox.showwarning("Atención", "No se encontró empleado con ese ID.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el empleado: {e}")
    finally:
        cursor.close()



# ====================== FUNCIONES PARA CULTIVOS ============================
def buscar_temporada():
    id_val = id_temporada.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID de la temporada para buscar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    success, result = db.call_procedure('sp_buscar_temporada', (id_val_int,))

    if not success:
        messagebox.showerror("Error", f"Error al buscar la temporada: {result}")
        return

    if result and len(result) > 0:
        fila = result[0]

        id_temporada.delete(0, "end")
        id_temporada.insert(0, fila[0])

        nombre_temporada.delete(0, "end")
        nombre_temporada.insert(0, fila[1])

        if fila[2]:
            fecha_inicio.set_date(fila[2])
        else:
            fecha_inicio.set_date('01/01/2000')

        if fila[3]:
            fecha_fin.set_date(fila[3])
        else:
            fecha_fin.set_date('01/01/2000')

        factor_multiplicador_tarifa.delete(0, "end")
        factor_multiplicador_tarifa.insert(0, fila[4] if fila[4] is not None else '')

        messagebox.showinfo("Éxito", "Temporada encontrada y datos cargados.")
    else:
        messagebox.showinfo("No encontrado", f"No se encontró ninguna temporada con ID {id_val_int}.")

def limpiar_temporadas():
    id_temporada.delete(0, "end")
    nombre_temporada.delete(0, "end")
    fecha_inicio.set_date('01/01/2000')
    fecha_fin.set_date('01/01/2000')
    factor_multiplicador_tarifa.delete(0, "end")

def borrar_temporada():
    id_val = id_temporada.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID de la temporada para eliminar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    confirm = messagebox.askyesno("Confirmar eliminación", f"¿Está seguro de eliminar la temporada con ID {id_val_int}?")
    if not confirm:
        return

    cursor = db.connection.cursor()
    try:
        cursor.callproc('sp_deleteTemporada', (id_val_int,))
        db.connection.commit()
        messagebox.showinfo("Éxito", "Temporada eliminada correctamente.")
        limpiar_temporadas()
        cargar_datos_temporadas()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar la temporada: {e}")
    finally:
        cursor.close()

def actualizar_temporada():
    id_val = id_temporada.get()
    if not id_val.strip():
        messagebox.showerror("Error", "Por favor ingrese el ID de la temporada para actualizar.")
        return

    try:
        id_val_int = int(id_val)
    except ValueError:
        messagebox.showerror("Error", "El ID debe ser un número entero.")
        return

    nombre_val = nombre_temporada.get().strip()
    fecha_inicio_val = fecha_inicio.get_date()
    fecha_fin_val = fecha_fin.get_date()

    factor_val = factor_multiplicador_tarifa.get().strip()
    try:
        factor_float = float(factor_val) if factor_val else 1.0
    except ValueError:
        messagebox.showerror("Error", "El factor multiplicador debe ser un número decimal.")
        return

    if not nombre_val:
        messagebox.showerror("Error", "El nombre de la temporada no puede estar vacío.")
        return

    cursor = db.connection.cursor()
    try:
        cursor.callproc('sp_updateTemporada', (
            id_val_int,
            nombre_val,
            fecha_inicio_val,
            fecha_fin_val,
            factor_float
        ))
        db.connection.commit()
        messagebox.showinfo("Éxito", "Temporada actualizada correctamente.")
        limpiar_temporadas()
        cargar_datos_temporadas()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar la temporada: {e}")
    finally:
        cursor.close()


def insertar_temporada():
    # Obtener datos desde los widgets
    nombre_val = nombre_temporada.get().strip()
    fecha_inicio_val = fecha_inicio.get_date()  # Asumiendo que usas DateEntry
    fecha_fin_val = fecha_fin.get_date()
    factor_val = factor_multiplicador_tarifa.get().strip()

    # Validar campos obligatorios
    if not nombre_val:
        messagebox.showerror("Error", "Por favor ingrese el nombre de la temporada.")
        return

    try:
        # Convertir factor a decimal (float)
        factor_float = float(factor_val)
    except ValueError:
        messagebox.showerror("Error", "El factor multiplicador debe ser un número válido.")
        return

    # Llamar al procedimiento almacenado con los parámetros
    success, result = db.call_procedure('sp_insertTemporada',
                                       (nombre_val, fecha_inicio_val, fecha_fin_val, factor_float))

    if success:
        messagebox.showinfo("Éxito", "Temporada insertada correctamente.")
    else:
        messagebox.showerror("Error", f"No se pudo insertar la temporada: {result}")




# =================== FUNCIONES DE EVENTOS PARA LISTAS ===================

def on_product_select(event):
    pass


def on_customer_select(event):
    pass


def on_employee_select(event):
    pass

#======================== pdf function ======================
def exportar_treeview_a_pdf(treeview, nombre_archivo="exportacion.pdf", titulo="Datos Exportados"):
    columnas = treeview["columns"]
    filas = [treeview.item(child)["values"] for child in treeview.get_children()]

    if not filas:
        messagebox.showwarning("Advertencia", "No hay datos para exportar.")
        return

    try:
        c = canvas.Canvas(nombre_archivo, pagesize=letter)
        width, height = letter
        x = 40
        y = height - 40

        # Título
        c.setFont("Helvetica-Bold", 14)
        c.drawString(x, y, titulo)
        y -= 30

        # Encabezados
        c.setFont("Helvetica-Bold", 10)
        for i, col in enumerate(columnas):
            c.drawString(x + i * 100, y, str(col))
        y -= 20

        # Datos
        c.setFont("Helvetica", 10)
        for fila in filas:
            for i, valor in enumerate(fila):
                c.drawString(x + i * 100, y, str(valor))
            y -= 20
            if y < 50:
                c.showPage()
                y = height - 40

        c.save()
        messagebox.showinfo("Éxito", f"PDF guardado correctamente en:\n{os.path.abspath(nombre_archivo)}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo exportar el PDF:\n{e}")




#========================= excel function====================

def exportar_treeview_a_excel(tree, default_filename="datos.xlsx"):
    # Obtener columnas
    cols = tree["columns"]
    # Obtener filas
    data = []
    for child in tree.get_children():
        data.append(tree.item(child)["values"])
    # Crear DataFrame
    df = pd.DataFrame(data, columns=cols)

    # Guardar archivo Excel con diálogo
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
                                             initialfile=default_filename)
    if file_path:
        try:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Exportar Excel", f"Datos exportados correctamente a:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar a Excel:\n{e}")



#========================== excel export =====================
def exportar_clientes_excel():
    exportar_treeview_a_excel(clientes_tree, "clientes.xlsx")

def exportar_empleados_excel():
    exportar_treeview_a_excel(empleados_tree, "empleados.xlsx")

def exportar_temporadas_excel():
    exportar_treeview_a_excel(temporadas_tree, "temporadas.xlsx")

def exportar_hoteles_excel():
    exportar_treeview_a_excel(hoteles_tree, "hoteles.xlsx")


#========================= pdf export =======================
def exportar_clientes_pdf():
    exportar_treeview_a_pdf(clientes_tree, nombre_archivo="clientes.pdf", titulo="Lista de Clientes")

def exportar_empleados_pdf():
    exportar_treeview_a_pdf(empleados_tree, nombre_archivo="empleados.pdf", titulo="Lista de Empleados")

def exportar_temporadas_pdf():
    exportar_treeview_a_pdf(temporadas_tree, nombre_archivo="temporadas.pdf", titulo="Lista de Temporadas")

def exportar_hoteles_pdf():
    exportar_treeview_a_pdf(hoteles_tree, nombre_archivo="hoteles.pdf", titulo="Lista de Hoteles")


# =================== INTERFAZ GRÁFICA ===================
# Crear la ventana principal
root = ctk.CTk()
root.geometry('1200x700')
root.title("PROYECTO #2")

root.iconbitmap("favicon.ico")

#================ imagenes para los botones ===================
imagen = Image.open("guardar.png")
imagen_redimensionada = imagen.resize((24, 24), Image.LANCZOS)
icono_guardar = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(24, 24))

imagen_actualizar=Image.open("actualizar.png")
imagen_redimensionada_a = imagen_actualizar.resize((24, 24), Image.LANCZOS)
icono_actualizar = ctk.CTkImage(light_image=imagen_actualizar, dark_image=imagen_actualizar, size=(24, 24))

imagen_borrar=Image.open("borrar.png")
imagen_redimensionada_b = imagen_borrar.resize((24, 24), Image.LANCZOS)
icono_borrar = ctk.CTkImage(light_image=imagen_borrar, dark_image=imagen_borrar, size=(24, 24))

imagen_limpiar=Image.open("limpiar.png")
imagen_redimensionada_l = imagen_limpiar.resize((24, 24), Image.LANCZOS)
icono_limpiar = ctk.CTkImage(light_image=imagen_limpiar, dark_image=imagen_limpiar, size=(24, 24))

imagen_buscar=Image.open("buscar.png")
imagen_redimensionada_bu = imagen_buscar.resize((24, 24), Image.LANCZOS)
icono_buscar = ctk.CTkImage(light_image=imagen_buscar, dark_image=imagen_buscar, size=(24, 24))





ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

# Conectar a la base de datos al iniciar
if not db.connect():
    root.destroy()
    exit()

# Crear el widget Notebook (pestañas)
notebook = ttk.Notebook(root)

# Crear los frames que irán dentro de las pestañas
tab1 = ctk.CTkFrame(notebook)
tab2 = ctk.CTkFrame(notebook)
tab3 = ctk.CTkFrame(notebook)
tab4 = ctk.CTkFrame(notebook)

# Añadir las pestañas al Notebook
notebook.add(tab1, text="hoteles")
notebook.add(tab2, text="clientes")
notebook.add(tab3, text="empleados")
notebook.add(tab4, text="temporadas")

# Empaquetar el Notebook para que se muestre en la ventana

notebook.pack(expand=True, fill="both")

# Crear carpeta para guardar las fotos
ruta_imagenes = "imagenes_empleados"
os.makedirs(ruta_imagenes, exist_ok=True)

#========= funcion para cambiar el color del fondo ===============

def cambiar_tema():
    modo_actual = ctk.get_appearance_mode()
    if modo_actual == "Light":
        ctk.set_appearance_mode("dark")
        root.configure(text="Tema actual: Oscuro")
        boton_fondo.configure(text="Cambiar fondo")
    else:
        ctk.set_appearance_mode("light")
        root.configure(text="Tema actual: Claro")
        boton_fondo.configure(text="Cambiar fondo")




# =================== PESTAÑA 1 (hoteles) ===================
# Crear frame principal para fincas
main_frame_hoteles = ctk.CTkFrame(tab1)
main_frame_hoteles.pack(fill="both", expand=True, padx=10, pady=10)

# Frame izquierdo para formulario
left_frame_hoteles = ctk.CTkFrame(main_frame_hoteles)
left_frame_hoteles.pack(side="left", fill="y", padx=(0, 10))

# Título
titulo = ctk.CTkLabel(left_frame_hoteles, text="GESTIÓN DE HOTELES", font=("algerian", 20, "bold"))
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame_hoteles = ctk.CTkFrame(left_frame_hoteles)
form_frame_hoteles.pack(pady=20, anchor="w", padx=20)

#================== validacion solo digitos==============
def solo_digitos(P):
    return P.isdigit() or P == ""

vcmd = (form_frame_hoteles.register(solo_digitos), '%P')

#======================== validacion maximo 15 caracteres=================
def max_15_caracteres(P):
    return len(P) <= 21 or len(P)<3

# Registrar función
vcmdmax = form_frame_hoteles.register(max_15_caracteres)


ctk.CTkLabel(form_frame_hoteles, text="ID_HOTEl:", font=("algerian", 18)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
idhotel = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18),validate='key',validatecommand=vcmd)
idhotel.grid(row=2, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_hoteles, text="NOMBRE_HOTEL:", font=("algerian", 18)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
nombre_hotel = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18))
nombre_hotel.grid(row=3, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_hoteles, text="CATEGORIA:", font=("algerian", 18)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
categoria = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18))
categoria.grid(row=4, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_hoteles, text="DIRECCION:", font=("algerian", 18)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
direccion = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18))
direccion.grid(row=5, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_hoteles, text="TELEFONO :", font=("algerian", 18)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
tel = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18),validate='key',validatecommand=vcmd)
tel.grid(row=6, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_hoteles, text="CORREO:", font=("algerian", 18)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=10)
correo = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18))
correo.grid(row=7, column=1, sticky="w", pady=10)


ctk.CTkLabel(form_frame_hoteles, text="AÑO_INAUGURACION:",font=("algerian",18)).grid(row=8, column=0, sticky="w", pady=5)
año_inauguracion = DateEntry(form_frame_hoteles, width=18, background='green', borderwidth=2, date_pattern='dd/mm/yyyy')
año_inauguracion.grid(row=8, column=1, sticky="w", padx=5, pady=5)


ctk.CTkLabel(form_frame_hoteles, text="HABITANTES:", font=("algerian", 18)).grid(row=9, column=0, sticky="w", padx=(0, 10), pady=10)
habitantes = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18))
habitantes.grid(row=9, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_hoteles, text="SERVICIOS:", font=("algerian", 18)).grid(row=10, column=0, sticky="w", padx=(0, 10), pady=10)
servicios = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18))
servicios.grid(row=10, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_hoteles, text="CHEK-IN-HORARIOS:", font=("algerian", 18)).grid(row=11, column=0, sticky="w", padx=(0, 10), pady=10)
checkin = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18))
checkin.grid(row=11, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_hoteles, text="CHECK-OUT-HORARIOS:", font=("algerian", 18)).grid(row=12, column=0, sticky="w", padx=(0, 10), pady=10)
checkout = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18))
checkout.grid(row=12, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_hoteles, text="GERENTE:", font=("algerian", 18)).grid(row=13, column=0, sticky="w", padx=(0, 10), pady=10)
gerente = ctk.CTkEntry(form_frame_hoteles, width=250, font=("algerian", 18))
gerente.grid(row=13, column=1, sticky="w", pady=10)

# Frame para botones
button_frame_hoteles = ctk.CTkFrame(left_frame_hoteles)
button_frame_hoteles.pack(pady=20)

btn_save_product = ctk.CTkButton(button_frame_hoteles, text="Guardar",width=70,image=icono_guardar,compound="left",command=guardar_hotel)
btn_save_product.pack(side=ctk.LEFT, padx=3)

btn_update_product = ctk.CTkButton(button_frame_hoteles, text="Actualizar",width=70,image=icono_actualizar,compound="left",command=actualizar_hotel)
btn_update_product.pack(side=ctk.LEFT, padx=3)

btn_delete_product = ctk.CTkButton(button_frame_hoteles, text="Eliminar",width=70,image=icono_borrar,compound="left",command=eliminar_hotel)
btn_delete_product.pack(side=tk.LEFT, padx=3)

btn_search_product = ctk.CTkButton(button_frame_hoteles, text="Buscar",width=70,image=icono_buscar,compound="left",command=buscar_hotel_por_id)
btn_search_product.pack(side=ctk.LEFT, padx=3)

btn_clear_product = ctk.CTkButton(button_frame_hoteles, text="Limpiar",width=70,image=icono_limpiar,compound="left",command=limpiar_campos_hoteles)
btn_clear_product.pack(side=ctk.LEFT, padx=3)

boton_fondo = ctk.CTkButton(button_frame_hoteles, text="Cambiar fondo", width=70,command=cambiar_tema)
boton_fondo.pack(pady=10)

btn_export_excel_fincas = ctk.CTkButton(button_frame_hoteles, text="Exportar Excel",command=exportar_hoteles_excel)
btn_export_excel_fincas.pack(side=ctk.LEFT, padx=3)

btn_export_pdf_fincas = ctk.CTkButton(button_frame_hoteles, text="Exportar PDF",command=exportar_hoteles_pdf)
btn_export_pdf_fincas.pack(side=ctk.LEFT, padx=3)



# Frame derecho para lista
right_frame_hoteles = ctk.CTkFrame(main_frame_hoteles)
right_frame_hoteles.pack(side="right", fill="both", expand=True)

ctk.CTkLabel(right_frame_hoteles, text="LISTA DE HOTELES", font=("algerian", 20, "bold")).pack(pady=10)

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="black",
                foreground="white",
                rowheight=25,
                font=('calibri', 11))

# Encabezados
style.configure("Treeview.Heading",
                background="black",
                foreground="green",
                font=('Arial', 12, 'bold'))



# Treeview para mostrar productos
hoteles_tree = ttk.Treeview(right_frame_hoteles, columns=('id_hotel', 'nombre_hotel', 'categoria', 'direccion', 'telefono', 'correo','año_inauguracion','numero_total_habitantes','servicios_disponibles','horarios_check_in','horarios_check_out','gerente_responsable'),show='headings', height=20)
hoteles_tree.heading('id_hotel', text='ID')
hoteles_tree.heading('nombre_hotel', text='Nombre')
hoteles_tree.heading('categoria', text='categoria')
hoteles_tree.heading('direccion',text='dicc')
hoteles_tree.heading('telefono', text='tel')
hoteles_tree.heading('correo', text='correo')
hoteles_tree.heading('año_inauguracion', text='inauguracion')
hoteles_tree.heading('numero_total_habitantes', text='habitantes')
hoteles_tree.heading('servicios_disponibles', text='servicios')
hoteles_tree.heading('horarios_check_in', text='horarios_check_in')
hoteles_tree.heading('horarios_check_out', text='horarios_check_out')
hoteles_tree.heading('gerente_responsable', text='gerente_responsable')


hoteles_tree.column('id_hotel', width=50)
hoteles_tree.column('nombre_hotel', width=70)
hoteles_tree.column('categoria', width=70)
hoteles_tree.column('direccion', width=70)
hoteles_tree.column('telefono',width=70)
hoteles_tree.column('correo', width=70)
hoteles_tree.column('año_inauguracion', width=70)
hoteles_tree.column('numero_total_habitantes', width=70)
hoteles_tree.column('servicios_disponibles', width=70)
hoteles_tree.column('horarios_check_in', width=70)
hoteles_tree.column('horarios_check_out', width=70)
hoteles_tree.column('gerente_responsable', width=70)


hoteles_tree.bind('<<TreeviewSelect>>', on_product_select)
hoteles_tree.pack(fill="both", expand=True, padx=10, pady=10)


# Crear Scrollbar vertical personalizada con CTk
scrollbar_hoteles = ctk.CTkScrollbar(hoteles_tree, orientation="vertical", command=hoteles_tree.yview)
hoteles_tree.configure(yscrollcommand=scrollbar_hoteles.set)

# Empaquetar ambos: Treeview a la izquierda, scrollbar a la derecha
hoteles_tree.pack(side="left", fill="both", expand=True)
scrollbar_hoteles.pack(side="right", fill="y")

scrollbar_hoteles .configure(
    fg_color="#2b2b2b",         # Fondo gris oscuro
    button_color="#2ecc71",     # Verde igual que los botones
    button_hover_color="#27ae60"
)
cargar_datos_hoteles()


# =================== PESTAÑA 2 (clientes) ===================
main_frame_clientes = ctk.CTkFrame(tab2)
main_frame_clientes.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_clientes = ctk.CTkFrame(main_frame_clientes)
left_frame_clientes.pack(side="left", fill="y", padx=(0, 10))

titulo2 = ctk.CTkLabel(left_frame_clientes, text="GESTIÓN DE CLIENTES", font=("algerian", 20, "bold"))
titulo2.pack(pady=20)

form_frame_clientes = ctk.CTkFrame(left_frame_clientes)
form_frame_clientes.pack(pady=20, anchor="w", padx=20)

ctk.CTkLabel(form_frame_clientes, text="id_cliente:", font=("algerian", 18)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
id_cliente = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18),validate='key',validatecommand=vcmd)
id_cliente.grid(row=1, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_clientes, text="nombre:", font=("algerian", 18)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
nombre = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18))
nombre.grid(row=2, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_clientes, text="apellido:",font=("algerian",18)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
apellido = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18))
apellido.grid(row=3, column=1, sticky="w", padx=5, pady=5)

ctk.CTkLabel(form_frame_clientes, text="documento_identidad:", font=("algerian", 18)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
documento_identidad = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18),validate='key',validatecommand=vcmd)
documento_identidad.grid(row=4, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_clientes, text="nacionalidad:", font=("algerian", 18)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
nacionalidad = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18))
nacionalidad.grid(row=5, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_clientes, text="fecha_nacimiento:", font=("algerian", 18)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
fecha_nacimiento = DateEntry(form_frame_clientes, width=18, background='green', borderwidth=2, date_pattern='dd/mm/yyyy')
fecha_nacimiento.grid(row=6, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_clientes, text="direccion:", font=("algerian", 18)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=10)
direccion_clientes = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18))
direccion_clientes.grid(row=7, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_clientes, text="telefono:", font=("algerian", 18)).grid(row=8, column=0, sticky="w", padx=(0, 10), pady=10)
telefono = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18),validate='key',validatecommand=vcmd)
telefono.grid(row=8, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_clientes, text="correo:", font=("algerian", 18)).grid(row=9, column=0, sticky="w", padx=(0, 10), pady=10)
correo = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18))
correo.grid(row=9, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_clientes, text="preferencias_especiales:", font=("algerian", 18)).grid(row=10, column=0, sticky="w", padx=(0, 10), pady=10)
preferencias_especiales = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18))
preferencias_especiales.grid(row=10, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_clientes, text="nivel_programa_fidelizacion:", font=("algerian", 18)).grid(row=11, column=0, sticky="w", padx=(0, 10), pady=10)
nivel_programa_fidelizacion = ctk.CTkEntry(form_frame_clientes, width=250, font=("algerian", 18))
nivel_programa_fidelizacion.grid(row=11, column=1, sticky="w", pady=10)



# Frame para botones de clientes
button_frame_clientes = ctk.CTkFrame(left_frame_clientes)
button_frame_clientes.pack(pady=20)

btn_save_customer = ctk.CTkButton(button_frame_clientes, text="Guardar",width=70,image=icono_guardar,compound="left",command=guardar_cliente)
btn_save_customer.pack(side=ctk.LEFT, padx=3)

btn_update_customer = ctk.CTkButton(button_frame_clientes, text="Actualizar",width=70,image=icono_actualizar,compound="left",command=actualizar_cliente)
btn_update_customer.pack(side=ctk.LEFT, padx=3)

btn_delete_customer = ctk.CTkButton (button_frame_clientes, text="Eliminar", width=70,image=icono_borrar,compound="left",command=eliminar_cliente)
btn_delete_customer.pack(side=ctk.LEFT, padx=3)

btn_search_customer = ctk.CTkButton(button_frame_clientes, text="Buscar",width=70,image=icono_buscar,compound="left",command=buscar_cliente)
btn_search_customer.pack(side=ctk.LEFT, padx=3)

btn_clear_customer = ctk.CTkButton(button_frame_clientes, text="Limpiar",width=70,image=icono_limpiar,compound="left",command=limpiar_campos_cliente)
btn_clear_customer.pack(side=tk.LEFT, padx=3)

boton_fondo = ctk.CTkButton(button_frame_clientes, text="Cambiar fondo",width=70, command=cambiar_tema)
boton_fondo.pack(pady=10)

btn_export_excel_clientes = ctk.CTkButton(button_frame_clientes, text="Exportar Excel",command=exportar_clientes_excel)
btn_export_excel_clientes.pack(side=ctk.LEFT, padx=3)

btn_export_pdf_clientes = ctk.CTkButton(button_frame_clientes, text="Exportar PDF",command=exportar_clientes_pdf)
btn_export_pdf_clientes.pack(side=ctk.LEFT, padx=3)

# Frame derecho para lista de customers
right_frame_clientes = ctk.CTkFrame(main_frame_clientes)
right_frame_clientes.pack(side="right", fill="both", expand=True)

ctk.CTkLabel(right_frame_clientes, text="LISTA DE CLIENTES", font=("algerian", 20, "bold")).pack(pady=10)

style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#2b2b2b",     # Fondo gris oscuro
                foreground="white",       # Texto blanco
                rowheight=25,
                fieldbackground="#2b2b2b",  # Asegura que el fondo interno también sea gris
                font=('Arial', 11))

# Encabezados
style.configure("Treeview.Heading",
                background="#2ecc71",  # Mismo verde que los botones
                foreground="white",
                font=('Arial', 12, 'bold'))



# Treeview para mostrar customers
clientes_tree = ttk.Treeview(right_frame_clientes,
                              columns=('id_cliente', 'nombre', 'apellido', 'documento_identidad', 'nacionalidad', 'fecha_nacimiento', 'direccion', 'telefono', 'correo', 'preferencias_especiales', 'nivel_programa_fidelizacion'),
                              show='headings', height=20)
clientes_tree.heading('id_cliente', text='ID')
clientes_tree.heading('nombre', text='nombre')
clientes_tree.heading('apellido', text='apellido')
clientes_tree.heading('documento_identidad', text='documento_identidad')
clientes_tree.heading('nacionalidad', text='nacionalidad')
clientes_tree.heading('fecha_nacimiento', text='fecha_nacimiento')
clientes_tree.heading('direccion', text='direccion')
clientes_tree.heading('telefono', text='telefono')
clientes_tree.heading('correo', text='correo')
clientes_tree.heading('preferencias_especiales', text='preferencias_especiales')
clientes_tree.heading('nivel_programa_fidelizacion', text='nivel_programa_fidelizacion')


clientes_tree.column('id_cliente', width=10)
clientes_tree.column('nombre', width=10)
clientes_tree.column('apellido', width=10)
clientes_tree.column('documento_identidad', width=10)
clientes_tree.column('nacionalidad', width=10)
clientes_tree.column('fecha_nacimiento', width=10)
clientes_tree.column('direccion', width=10)
clientes_tree.column('telefono', width=10)
clientes_tree.column('correo', width=10)
clientes_tree.column('preferencias_especiales', width=10)
clientes_tree.column('nivel_programa_fidelizacion', width=10)


clientes_tree.bind('<<TreeviewSelect>>', on_customer_select)
clientes_tree.pack(fill="both", expand=True, padx=10, pady=10)



# Crear Scrollbar vertical personalizada con CTk
scrollbar_customers = ctk.CTkScrollbar(clientes_tree, orientation="vertical", command=clientes_tree.yview)
clientes_tree.configure(yscrollcommand=scrollbar_customers.set)


# Empaquetar ambos: Treeview a la izquierda, scrollbar a la derecha
clientes_tree.pack(side="left", fill="both", expand=True)
scrollbar_customers.pack(side="right", fill="y")

scrollbar_customers.configure(
    fg_color="#2b2b2b",
    button_color="#2ecc71",
    button_hover_color="#27ae60"
)
cargar_datos_clientes()

# =================== PESTAÑA 3 (empleados) ===================
main_frame_empleados = ctk.CTkFrame (tab3)
main_frame_empleados.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_empleados = ctk.CTkFrame(main_frame_empleados)
left_frame_empleados.pack(side="left", fill="y", padx=(0, 10))

titulo3 = ctk.CTkLabel(left_frame_empleados, text="GESTIÓN DE EMPLEADOS", font=("algerian", 20, "bold"))
titulo3.pack(pady=20)

form_frame_empleados = ctk.CTkFrame(left_frame_empleados)
form_frame_empleados.pack(pady=20, anchor="w", padx=20)

ctk.CTkLabel(form_frame_empleados, text="id_empleado:", font=("algerian", 18)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
id_empleado = ctk.CTkEntry(form_frame_empleados, width=250, font=("algerian", 18),validate='key',validatecommand=vcmd)
id_empleado.grid(row=1, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_empleados, text="nombres:", font=("algerian", 18)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
nombres = ctk.CTkEntry(form_frame_empleados, width=250, font=("algerian", 18))
nombres.grid(row=2, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_empleados, text="apellidos:", font=("algerian", 18)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
apellidos = ctk.CTkEntry(form_frame_empleados, width=250, font=("algerian", 18))
apellidos.grid(row=3, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_empleados, text="cargo:", font=("algerian", 18)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
cargo = ctk.CTkEntry(form_frame_empleados, width=250, font=("algerian", 18))
cargo.grid(row=4, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_empleados, text="telefono:",font=('algerian',18)).grid(row=5,column=0,sticky="w", padx=(0, 10), pady=10)
telefono = ctk.CTkEntry(form_frame_empleados, width=250, font=("algerian", 18))
telefono.grid(row=5, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_empleados, text="correo :", font=("algerian", 18)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
correo = ctk.CTkEntry(form_frame_empleados, width=250, font=("algerian", 18))
correo.grid(row=6, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_empleados, text="id_hotel :", font=("algerian", 18)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=10)
id_hotel = ctk.CTkEntry(form_frame_empleados, width=250, font=("algerian", 18),validate='key',validatecommand=vcmd)
id_hotel.grid(row=7, column=1, sticky="w", pady=10)


# Frame para botones de empleados
button_frame_empleados = ctk.CTkFrame(left_frame_empleados)
button_frame_empleados.pack(pady=20)

btn_save_employee = ctk.CTkButton(button_frame_empleados, text="Guardar",width=70,image=icono_guardar,compound="left",command=guardar_empleado)
btn_save_employee.pack(side=tk.LEFT, padx=3)

btn_update_employee = ctk.CTkButton(button_frame_empleados, text="Actualizar", width=70,image=icono_actualizar,compound="left",command=actualizar_empleado)
btn_update_employee.pack(side=tk.LEFT, padx=3)

btn_delete_employee = ctk.CTkButton(button_frame_empleados, text="Eliminar",width=70,image=icono_borrar,compound="left",command=eliminar_empleado)
btn_delete_employee.pack(side=tk.LEFT, padx=3)

btn_search_employee = ctk.CTkButton(button_frame_empleados, text="Buscar",width=70,image=icono_buscar,compound="left",command=buscar_empleado)
btn_search_employee.pack(side=tk.LEFT, padx=3)

btn_clear_employee = ctk.CTkButton(button_frame_empleados, text="Limpiar",width=70,image=icono_limpiar,compound="left",command=limpiar_empleado)
btn_clear_employee.pack(side=tk.LEFT, padx=3)


boton_fondo = ctk.CTkButton(button_frame_empleados, text="Cambiar fondo",width=70 ,command=cambiar_tema)
boton_fondo.pack(pady=10)

btn_exportar_empleados_pdf = ctk.CTkButton(button_frame_empleados, text="Exportar PDF",command=exportar_empleados_pdf)
btn_exportar_empleados_pdf.pack(side=tk.LEFT, padx=3)

btn_exportar_empleados_excel = ctk.CTkButton(button_frame_empleados, text="Exportar Excel",command=exportar_empleados_excel)
btn_exportar_empleados_excel.pack(side=tk.LEFT, padx=3)



# Frame derecho para lista de empleados
right_frame_empleados = ctk.CTkFrame(main_frame_empleados)
right_frame_empleados.pack(side="right", fill="both", expand=True)

# Título
ctk.CTkLabel(right_frame_empleados, text="LISTA DE EMPLEADOS", font=("Algerian", 20, "bold")).pack(pady=10)

# Frame contenedor para Treeview y Scrollbar
tree_container = ctk.CTkFrame(right_frame_empleados)
tree_container.pack(fill="both", expand=True, padx=10, pady=10)

# Estilo para Treeview
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#2b2b2b",
                foreground="white",
                rowheight=25,
                fieldbackground="#2b2b2b",
                font=('Arial', 11))

style.configure("Treeview.Heading",
                background="#2ecc71",
                foreground="white",
                font=('Arial', 12, 'bold'))

# Crear el Treeview
empleados_tree = ttk.Treeview(tree_container,
                              columns=('id_empleados', 'nombres', 'apellidos', 'cargo', 'telefono', 'correo','id_hotel'),
                              show='headings', height=20)

empleados_tree.heading('id_empleados', text='id')
empleados_tree.heading('nombres', text='nombres')
empleados_tree.heading('apellidos', text='apellidos')
empleados_tree.heading('cargo', text=' cargo')
empleados_tree.heading('telefono', text='telefono')
empleados_tree.heading('correo', text='correo')
empleados_tree.heading('id_hotel', text='id_hotel')


empleados_tree.column('id_empleados', width=50)
empleados_tree.column('nombres', width=80)
empleados_tree.column('apellidos', width=80)
empleados_tree.column('cargo', width=100)
empleados_tree.column('telefono', width=80)
empleados_tree.column('correo', width=150)
empleados_tree.column('id_hotel', width=60)

empleados_tree.bind('<<TreeviewSelect>>', on_employee_select)

# Crear Scrollbar vertical personalizada con CTk
scrollbar_empleados = ctk.CTkScrollbar(tree_container, orientation="vertical", command=empleados_tree.yview)
empleados_tree.configure(yscrollcommand=scrollbar_empleados.set)


# Empaquetar Treeview y Scrollbar correctamente
empleados_tree.pack(side="left", fill="both", expand=True)
scrollbar_empleados.pack(side="right", fill="y")



# Estilizar scrollbar
scrollbar_empleados.configure(
    fg_color="#2b2b2b",         # Fondo gris oscuro
    button_color="#2ecc71",     # Verde botón
    button_hover_color="#27ae60"
)

cargar_datos_empleados()



#==================== pestaña #4 (temporadas)=====================
main_frame_temporadas = ctk.CTkFrame (tab4)
main_frame_temporadas.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_temporadas = ctk.CTkFrame(main_frame_temporadas)
left_frame_temporadas.pack(side="left", fill="y", padx=(0, 10))

titulo4 = ctk.CTkLabel(left_frame_temporadas, text="GESTIÓN DE TEMPORADAS", font=("algerian", 20, "bold"))
titulo4.pack(pady=20)

form_frame_temporadas = ctk.CTkFrame(left_frame_temporadas)
form_frame_temporadas.pack(pady=20, anchor="w", padx=20)

ctk.CTkLabel(form_frame_temporadas, text="id_temporada:", font=("algerian", 18)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
id_temporada = ctk.CTkEntry(form_frame_temporadas, width=250, font=("algerian", 18),validate='key',validatecommand=vcmd)
id_temporada.grid(row=1, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_temporadas, text="nombre_temporada:", font=("algerian", 18)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
nombre_temporada = ctk.CTkEntry(form_frame_temporadas, width=250, font=("algerian", 18) )
nombre_temporada.grid(row=2, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_temporadas, text="fecha_inicio:", font=("algerian", 18)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
fecha_inicio = DateEntry(form_frame_temporadas, width=18, background='green', borderwidth=2, date_pattern='dd/mm/yyyy')
fecha_inicio.grid(row=3, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_temporadas, text="fecha_fin(dd):", font=("algerian", 18)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
fecha_fin = DateEntry(form_frame_temporadas, width=18, background='green', borderwidth=2, date_pattern='dd/mm/yyyy')
fecha_fin.grid(row=5, column=1, sticky="w", pady=10)

ctk.CTkLabel(form_frame_temporadas, text="factor_multiplicador_tarifa :", font=("algerian", 18)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
factor_multiplicador_tarifa = ctk.CTkEntry(form_frame_temporadas, width=250, font=("algerian", 18))
factor_multiplicador_tarifa.grid(row=6, column=1, sticky="w", pady=10)


# Frame para botones de employees
button_frame_temporadas = ctk.CTkFrame(left_frame_temporadas)
button_frame_temporadas.pack(pady=20)

btn_save_temporadas = ctk.CTkButton(button_frame_temporadas, text="Guardar",width=70,image=icono_guardar,compound="left",command=insertar_temporada)
btn_save_temporadas.pack(side=tk.LEFT, padx=3)

btn_update_temporadas = ctk.CTkButton(button_frame_temporadas, text="Actualizar", width=70,image=icono_actualizar,compound="left",command=actualizar_temporada)
btn_update_temporadas.pack(side=tk.LEFT, padx=3)

btn_delete_temporadas = ctk.CTkButton(button_frame_temporadas, text="Eliminar",width=70,image=icono_borrar,compound="left",command=borrar_temporada)
btn_delete_temporadas.pack(side=tk.LEFT, padx=3)

btn_search_temporadas = ctk.CTkButton(button_frame_temporadas, text="Buscar",width=70,image=icono_buscar,compound="left",command=buscar_temporada)
btn_search_temporadas.pack(side=tk.LEFT, padx=3)

btn_clear_temporadas = ctk.CTkButton(button_frame_temporadas, text="Limpiar",width=70,image=icono_limpiar,compound="left",command=limpiar_temporadas)
btn_clear_temporadas.pack(side=tk.LEFT, padx=3)

boton_fondo = ctk.CTkButton(button_frame_temporadas, text="Cambiar fondo",width=70 ,command=cambiar_tema)
boton_fondo.pack(pady=10)

btn_exportar_temporadas_pdf = ctk.CTkButton(button_frame_temporadas, text="Exportar PDF",command=exportar_temporadas_pdf)
btn_exportar_temporadas_pdf.pack(side=tk.LEFT, padx=3)

btn_exportar_temporadas_excel = ctk.CTkButton(button_frame_temporadas, text="Exportar Excel",command=exportar_temporadas_excel)
btn_exportar_temporadas_excel.pack(side=tk.LEFT, padx=3)


# frame para temporadas
right_frame_temporadas = ctk.CTkFrame(main_frame_temporadas)
right_frame_temporadas.pack(side="right", fill="both", expand=True)

# Título
ctk.CTkLabel(right_frame_temporadas, text="LISTA DE TEMPORADAS", font=("Algerian", 20, "bold")).pack(pady=10)

# Frame contenedor para Treeview y Scrollbar
tree_container = ctk.CTkFrame(right_frame_temporadas)
tree_container.pack(fill="both", expand=True, padx=10, pady=10)

# Estilo para Treeview
style = ttk.Style()
style.theme_use("default")

style.configure("Treeview",
                background="#2b2b2b",
                foreground="white",
                rowheight=25,
                fieldbackground="#2b2b2b",
                font=('Arial', 11))

style.configure("Treeview.Heading",
                background="#2ecc71",
                foreground="white",
                font=('Arial', 12, 'bold'))

# Crear el Treeview
temporadas_tree = ttk.Treeview(tree_container,
                              columns=('id_temporada', 'nombre_temporada', 'fecha_inicio', 'fecha_fin', 'factor_multiplicador_tarifa'),
                              show='headings', height=20)

temporadas_tree.heading('id_temporada', text='id_temporada')
temporadas_tree.heading('nombre_temporada', text='nombre_temporada')
temporadas_tree.heading('fecha_inicio', text='fecha_inicio')
temporadas_tree.heading('fecha_fin', text=' fecha_fin')
temporadas_tree.heading('factor_multiplicador_tarifa', text='factor_multiplicador_tarifa')

temporadas_tree.column('id_temporada', width=50)
temporadas_tree.column('nombre_temporada', width=50)
temporadas_tree.column('fecha_inicio', width=50)
temporadas_tree.column('fecha_fin', width=50)
temporadas_tree.column('factor_multiplicador_tarifa', width=50)



# Crear Scrollbar vertical personalizada con CTk
scrollbar_cultivos = ctk.CTkScrollbar(tree_container, orientation="vertical", command=temporadas_tree.yview)
temporadas_tree.configure(yscrollcommand=scrollbar_cultivos.set)


# Empaquetar Treeview y Scrollbar correctamente
temporadas_tree.pack(side="left", fill="both", expand=True)
scrollbar_cultivos.pack(side="right", fill="y")



# Estilizar scrollbar
scrollbar_cultivos.configure(
    fg_color="#2b2b2b",         # Fondo gris oscuro
    button_color="#2ecc71",     # Verde botón
    button_hover_color="#27ae60"
)

cargar_datos_temporadas()


# =================== CARGAR DATOS INICIALES ===================
def load_initial_data():
    pass


# Cargar datos al iniciar
root.after(1000, load_initial_data)  # Cargar después de 1 segundo


# =================== FUNCIÓN DE CIERRE ===================
def on_closing():
    db.disconnect()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

# Ejecutar la aplicación
root.mainloop()
import psycopg
import sys 

# --- Configuración de la Base de Datos ---

DB_HOST = "localhost"
DB_NAME = "clientes"
DB_USER = "postgres"
DB_PASSWORD = "123" 

# --- Función para Conectar a la Base de Datos ---
def conectar():
    """
    Establece y devuelve una conexión a la base de datos PostgreSQL.
    Maneja errores de conexión.
    """
    conexion = None
    try:
        # Intenta conectar a la base de datos
        conexion = psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        print("Conexión a la base de datos exitosa.")
        return conexion
    except psycopg.OperationalError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
    except Exception as e:
        print(f"Ocurrió un error inesperado al conectar: {e}")
        return None

# --- Función para Crear un Nuevo Registro ---
def crear_dato(ci, nombre, apellido):
    """
    Inserta un nuevo registro en la tabla datos_personales.
    """
    conexion = conectar()
    if conexion:
        cursor = None
        try:
            cursor = conexion.cursor()
            # Consulta SQL para insertar datos, usando marcadores de posición (%s)
            sql = "INSERT INTO public.datos_personales (ci, nombre, apellido) VALUES (%s, %s, %s)"
            cursor.execute(sql, (ci, nombre, apellido))
            conexion.commit() # Guarda los cambios en la base de datos 
            print(f"Registro creado exitosamente: CI={ci}, Nombre={nombre}, Apellido={apellido}")
        except psycopg.Error as e:
            print(f"Error al crear registro: {e}")
            conexion.rollback() # Revierte los cambios si hay un error
        except Exception as e:
            print(f"Ocurrió un error inesperado al crear registro: {e}")
            conexion.rollback()
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    else:
        print("No se pudo conectar para crear el registro.")

# --- Función para Leer (Obtener) Registros ---
def leer_datos():
    """
    Lee y muestra todos los registros de la tabla datos_personales.
    """
    conexion = conectar()
    if conexion:
        cursor = None
        try:
            cursor = conexion.cursor()
            sql = "SELECT ci, nombre, apellido FROM public.datos_personales"
            cursor.execute(sql)
            registros = cursor.fetchall() # Obtiene todas las filas 
            if registros:
                print("\n--- Registros en la Base de Datos ---")
                for reg in registros:
                    print(f"CI: {reg[0]}, Nombre: {reg[1]}, Apellido: {reg[2]}")
                print("------------------------------------")
            else:
                print("\nNo hay registros en la tabla datos_personales.")
            return registros
        except psycopg.Error as e:
            print(f"Error al leer registros: {e}")
            return None
        except Exception as e:
            print(f"Ocurrió un error inesperado al leer registros: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    else:
        print("No se pudo conectar para leer los registros.")
        return None

# --- Función para Actualizar un Registro ---
def actualizar_dato(ci, nuevo_nombre, nuevo_apellido):
    """
    Actualiza el nombre y apellido de un registro existente por su CI.
    """
    conexion = conectar()
    if conexion:
        cursor = None
        try:
            cursor = conexion.cursor()
            sql = "UPDATE public.datos_personales SET nombre = %s, apellido = %s WHERE ci = %s"
            cursor.execute(sql, (nuevo_nombre, nuevo_apellido, ci))
            conexion.commit()
            if cursor.rowcount > 0: # Verifica si se afectó alguna fila 
                print(f"Registro con CI {ci} actualizado exitosamente.")
            else:
                print(f"No se encontró ningún registro con CI {ci} para actualizar.")
        except psycopg.Error as e:
            print(f"Error al actualizar registro: {e}")
            conexion.rollback()
        except Exception as e:
            print(f"Ocurrió un error inesperado al actualizar registro: {e}")
            conexion.rollback()
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    else:
        print("No se pudo conectar para actualizar el registro.")

# --- Función para Borrar un Registro ---
def borrar_dato(ci):
    """
    Borra un registro de la tabla datos_personales por su CI.
    """
    conexion = conectar()
    if conexion:
        cursor = None
        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM public.datos_personales WHERE ci = %s"
            cursor.execute(sql, (ci,)) # La coma es importante para tuplas de un solo elemento 
            conexion.commit()
            if cursor.rowcount > 0: # Verifica si se afectó alguna fila 
                print(f"Registro con CI {ci} borrado exitosamente.")
            else:
                print(f"No se encontró ningún registro con CI {ci} para borrar.")
        except psycopg.Error as e:
            print(f"Error al borrar registro: {e}")
            conexion.rollback()
        except Exception as e:
            print(f"Ocurrió un error inesperado al borrar registro: {e}")
            conexion.rollback()
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()
    else:
        print("No se pudo conectar para borrar el registro.")

# --- Bloque Principal de Ejecución (Demostración CRUD) ---
if __name__ == "__main__":
    print("\n--- Demostración de Operaciones CRUD ---")

     # Datos de ejemplo
    ci_ejemplo = "1234567890"
    nombre_ejemplo = "Juan"
    apellido_ejemplo = "Pérez"

    # 1. Crear un registro
    print("\n--- 1. Creando un nuevo registro ---")
    crear_dato(ci_ejemplo, nombre_ejemplo, apellido_ejemplo)

    # 2. Leer registros
    print("\n--- 2. Leyendo todos los registros ---")
    leer_datos()

    # 3. Actualizar un registro
    print("\n--- 3. Actualizando el registro ---")
    actualizar_dato(ci_ejemplo, "Juanito", "Pérez García")

    # 4. Leer registros nuevamente para ver el cambio
    print("\n--- 4. Leyendo registros después de actualizar ---")
    leer_datos()

    # 5. Borrar un registro
    print("\n--- 5. Borrando el registro ---")
    borrar_dato(ci_ejemplo)

    #6. Leer registros por última vez para confirmar el borrado
    print("\n--- 6. Leyendo registros después de borrar ---")
     leer_datos()

    print("\n--- Demostración CRUD Finalizada ---")
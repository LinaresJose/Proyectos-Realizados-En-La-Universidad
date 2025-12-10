# --- Importaciones de todas las librerías que se usarán. ---

import dearpygui.dearpygui as dpg 
import requests 
from bs4 import BeautifulSoup # Para parsear HTML (web scraping) 
import psycopg 
import datetime # Para el timestamp de la fecha de raspado

# --- 1. Configuración de la Base de Datos ---

DB_HOST = "localhost" 
DB_NAME = "clientes" 
DB_USER = "postgres" 
DB_PASSWORD = "123" 

# --- 2. Funciones de Base de Datos ---

def insertar_articulo(url_origen, titulo, descripcion):
    conectar = None 
    try:
        conectar = psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conectar.cursor() 
        # Consulta SQL para insertar datos
        sql ="""
        INSERT INTO articulos_raspados (url_origen, titulo, descripcion) VALUES (%s, %s, %s);
        """
        cursor.execute(sql, (url_origen, titulo, descripcion)) 
        conectar.commit()
        cursor.close() 
        return True
    except psycopg.OperationalError as e:
        actualizar_estado_gui(f"Error de conexión a la BD: {e}", "rojo")
        return False
    except psycopg.Error as e:
        actualizar_estado_gui(f"Error al insertar en la BD: {e}", "rojo")
        return False
    finally:
        if conectar: 
            conectar.close() 

def obtener_urls_unicas():
    """
    Obtiene todas las URLs únicas de la tabla articulos_raspados.
    Retorna una lista de cadenas de URL.
    """
    conectar = None 
    urls_unicas = []
    try:
        conectar = psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conectar.cursor()
        sql = "SELECT DISTINCT url_origen FROM articulos_raspados ORDER BY url_origen;"
        cursor.execute(sql) 
        urls_unicas = [row[0] for row in cursor.fetchall()]
        cursor.close() 
    except psycopg.OperationalError as e:
        actualizar_estado_gui(f"Error de conexión a la BD al obtener URLs: {e}", "rojo")
    except psycopg.Error as e:
        actualizar_estado_gui(f"Error al obtener URLs de la BD: {e}", "rojo")
    finally:
        if conectar: 
            conectar.close() 
    return urls_unicas

def eliminar_articulos_por_url(url_a_eliminar):
    """
    Elimina todos los artículos asociados a una URL específica de la base de datos.
    """
    conectar = None 
    try:
        conectar = psycopg.connect(host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = conectar.cursor() 
        sql = "DELETE FROM articulos_raspados WHERE url_origen = %s;"
        cursor.execute(sql, (url_a_eliminar,)) 
        conectar.commit() 
        cursor.close()
        actualizar_estado_gui(f"URL '{url_a_eliminar}' y sus artículos eliminados de la BD.", "verde")
        return True
    except psycopg.OperationalError as e:
        actualizar_estado_gui(f"Error de conexión a la BD al eliminar URL: {e}", "rojo")
        return False
    except psycopg.Error as e:
        actualizar_estado_gui(f"Error al eliminar URL de la BD: {e}", "rojo")
        return False
    finally:
        if conectar: 
            conectar.close() 

# --- 3. Funciones de Web Scraping ---

def raspar_pagina_web(url):
    """
    Descarga el contenido de la URL y extrae títulos y párrafos de artículos.
    Retorna una lista de diccionarios con {'titulo', 'descripcion'}.
    """
    try:
        actualizar_estado_gui(f"Scrapeando: {url}...", "azul")
        
        pagina_descargada = requests.get(url, timeout=10) # Se Añade timeout para evitar esperas infinitas
        pagina_descargada.raise_for_status() # Lanza excepción para códigos de error HTTP (4xx o 5xx)
        html_content = pagina_descargada.text
        
        mapear_pagina = BeautifulSoup(html_content, 'html.parser') # Parsear HTML 
        
        articulos_encontrados = []
        
        # --- Lógica de extracción de datos ---
        
        # Buscar divs con la clase 'articulo' 
        articulos_divs = mapear_pagina.find_all('div', class_='articulo') 
        
        if not articulos_divs:
            actualizar_estado_gui("No se encontraron elementos con la clase 'articulo'. Intentando búsqueda más general...", "naranja")
            # Si no se encuentra la clase 'articulo', intentar una búsqueda más genérica
            # para al menos obtener algún h2 y p. Esto es para ser más robusto.
            
            # Buscar todos los h2 y los p en la página
            titulos = mapear_pagina.find_all('h2') 
            parrafos = mapear_pagina.find_all('p') 

            # Intenta emparejar h2 con el p siguiente o cercano
            for i, titulo_tag in enumerate(titulos):
                titulo_texto = titulo_tag.text.strip() # Extrae el texto 
                descripcion_texto = "No se encontró descripción cercana."
                
                # Busca el primer párrafo que sea 'hermano' o esté 'después' del h2
                next_p = titulo_tag.find_next_sibling('p') 
                if next_p:
                    descripcion_texto = next_p.text.strip()
                else: # Si no hay un p hermano, busca el primer p en general
                    if i < len(parrafos):
                        descripcion_texto = parrafos[i].text.strip()

                articulos_encontrados.append({
                    "titulo": titulo_texto,
                    "descripcion": descripcion_texto
                })
        else:
            for articulo in articulos_divs:
                titulo_articulo = articulo.find('h2') # Buscar el h2 dentro del div 
                parrafo_articulo = articulo.find('p') # Buscar el p dentro del div 

                titulo = titulo_articulo.text.strip() if titulo_articulo else "N/A"
                descripcion = parrafo_articulo.text.strip() if parrafo_articulo else "N/A"
                
                articulos_encontrados.append({
                    "titulo": titulo,
                    "descripcion": descripcion
                })

        if not articulos_encontrados:
            actualizar_estado_gui("No se pudieron extraer títulos y descripciones. La estructura de la página es inesperada.", "naranja")
            
        return articulos_encontrados

    except requests.exceptions.MissingSchema: # Errores de URL mal formada 
        actualizar_estado_gui("Error: URL inválida. Asegúrate de incluir 'http://' o 'https://'.", "rojo")
        return []
    except requests.exceptions.ConnectionError: # Errores de conexión de red 
        actualizar_estado_gui("Error de conexión: No se pudo conectar a la URL. Verifica tu conexión a internet o la URL.", "rojo")
        return []
    except requests.exceptions.Timeout: # Error de tiempo de espera 
        actualizar_estado_gui("Error de tiempo de espera: La solicitud tardó demasiado en responder.", "rojo")
        return []
    except requests.exceptions.RequestException as e: # Otros errores de requests 
        actualizar_estado_gui(f"Error al obtener la página web: {e}", "rojo")
        return []
    except Exception as e: # Cualquier otro error inesperado 
        actualizar_estado_gui(f"Error inesperado durante el scraping: {e}", "rojo")
        return []

# --- 4. Lógica de la GUI (DearPyGui) ---

# Función para actualizar el área de mensajes de la GUI
def actualizar_estado_gui(mensaje, color="blanco"):
    """Actualiza el texto del área de mensajes de la GUI con un color."""
    dpg.set_value("estado_text", mensaje)
    # Define colores para los mensajes
    if color == "rojo":
        dpg.bind_item_theme("estado_text", "error_theme")
    elif color == "verde":
        dpg.bind_item_theme("estado_text", "success_theme")
    elif color == "azul":
        dpg.bind_item_theme("estado_text", "info_theme")
    elif color == "naranja":
        dpg.bind_item_theme("estado_text", "warning_theme")
    else:
        dpg.bind_item_theme("estado_text", "default_text_theme")


def mostrar_resultados_gui(resultados):
    """Muestra los resultados raspados en el área de visualización de la GUI."""
    # Limpia los resultados anteriores
    if dpg.does_item_exist("resultados_group"):
        dpg.delete_item("resultados_group", children_only=True)

    if not resultados:
        dpg.add_text("No se encontraron datos para mostrar.", parent="resultados_group")
        return

    for i, item in enumerate(resultados):
        # Crear un grupo expandible para cada artículo para mejor visualización
        with dpg.tree_node(label=f"Artículo {i+1}: {item['titulo']}", parent="resultados_group"):
            dpg.add_text(f"Título: {item['titulo']}")
            dpg.add_text(f"Descripción: {item['descripcion']}")             

# Callback para el botón "Scrapear y Guardar Datos" 
def boton_scrapear_callback():
    url = dpg.get_value("url_input") # Obtener la URL del campo de texto 
    
    if not url:
        actualizar_estado_gui("Por favor, introduce una URL.", "naranja")
        return

    actualizar_estado_gui("Iniciando operación de scraping...", "azul")
    
    # Realizar el scraping
    articulos = raspar_pagina_web(url)
    
    if articulos:
        # Mostrar en la GUI
        mostrar_resultados_gui(articulos)
        
       # Guardar en la base de datos
        guardado_exitoso = True 
        for articulo in articulos:
            if not insertar_articulo(url, articulo['titulo'], articulo['descripcion']):
                guardado_exitoso = False 
                break # Si falla una inserción, no intentes el resto

        if guardado_exitoso:
            actualizar_estado_gui(f"Scraping completado y {len(articulos)} artículos guardados en la BD exitosamente.", "verde")
        else:
            actualizar_estado_gui(f"Scraping completado, pero hubo errores al guardar algunos artículos en la BD.", "naranja")
    else:
        actualizar_estado_gui("Scraping completado, pero no se encontraron datos para guardar.", "naranja")
        
# Callback para el botón "eliminar una URL específica" 
def accion_eliminar_url(sender, app_data, user_data):
    """
    Callback para el botón de eliminar una URL específica.
    user_data contendrá la URL a eliminar.
    """
    url_a_eliminar = user_data
    actualizar_estado_gui(f"Intentando eliminar URL: {url_a_eliminar}...", "azul")
    if eliminar_articulos_por_url(url_a_eliminar):
        # Si la eliminación fue exitosa, refresca la lista de URLs
        boton_ver_urls_callback()
    else:
        actualizar_estado_gui(f"Fallo al eliminar URL: {url_a_eliminar}.", "rojo")
        
# Callback para el botón "Ver URLs Guardadas" 
def boton_ver_urls_callback():
    """
    Callback para el botón "Ver URLs Guardadas".
    Obtiene y muestra las URLs únicas en una nueva ventana.
    """
    urls = obtener_urls_unicas()
    
    if dpg.does_item_exist("urls_guardadas_window"):
        dpg.delete_item("urls_guardadas_window", children_only=True)
    else:
        # Crear la ventana
        with dpg.window(label="URLs Guardadas", tag="urls_guardadas_window", width=600, height=400, show=False):
            pass # Se llenará dinámicamente

    # Mostrar la ventana
    dpg.show_item("urls_guardadas_window")
    dpg.set_item_pos("urls_guardadas_window", [100, 100]) # Posicionar la ventana

    if not urls:
        dpg.add_text("No hay URLs guardadas en la base de datos.", parent="urls_guardadas_window")
        actualizar_estado_gui("No se encontraron URLs guardadas.", "naranja")
    else:
        dpg.add_text("URLs guardadas (haz clic en Eliminar para borrarla):", parent="urls_guardadas_window")
        for url in urls:
            with dpg.group(horizontal=True, parent="urls_guardadas_window"):
                dpg.add_text(url, wrap=0) # wrap=0 para que la URL no se corte
                dpg.add_spacer(width=5)
                # El user_data del botón contendrá la URL a eliminar
                dpg.add_button(label="Eliminar", callback=accion_eliminar_url, user_data=url)
        actualizar_estado_gui(f"Mostrando {len(urls)} URLs guardadas.", "azul")
        
# Callback para el botón "Limpiar Resultados y URL" 
def boton_limpiar_gui_callback():
    """
    Callback para el botón "Limpiar Resultados y URL".
    Limpia el campo de URL y el área de resultados.
    """
    dpg.set_value("url_input", "") # Limpia el campo de entrada de URL
    if dpg.does_item_exist("resultados_group"):
        dpg.delete_item("resultados_group", children_only=True)
        dpg.add_text("Los resultados aparecerán aquí.", tag="placeholder_resultados", parent="resultados_group")
    actualizar_estado_gui("GUI limpia. Listo para una nueva URL.", "azul")
        
# --- 5. Función Principal y Configuración de DearPyGui ---
def main():
    dpg.create_context()
    dpg.create_viewport(title='Web Scraper con Python y PostgreSQL', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport() # El viewport debe estar "mostrado" para que get_viewport_width funcione correctamente.

    spacer_width_for_centering = dpg.get_viewport_width() / 2 - 310

    # --- Temas de colores para los mensajes de estado ---
    with dpg.theme(tag="error_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 0, 0, 255]) # Rojo
    with dpg.theme(tag="success_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 255, 0, 255]) # Verde
    with dpg.theme(tag="info_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 200, 255, 255]) # Azul claro
    with dpg.theme(tag="warning_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 165, 0, 255]) # Naranja
    with dpg.theme(tag="default_text_theme"):
        with dpg.theme_component(dpg.mvAll):
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255]) # Blanco por defecto
            
    # --- Tema para Botones ---
    with dpg.theme(tag="llamative_button_theme"):
        with dpg.theme_component(dpg.mvButton): # mvButton para aplicar al botón
            dpg.add_theme_color(dpg.mvThemeCol_Button, [60, 150, 255, 255])  # Azul brillante para el fondo
            dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, [80, 170, 255, 255]) # Un poco más claro al pasar el ratón
            dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, [40, 130, 235, 255])  # Un poco más oscuro al hacer clic
            dpg.add_theme_color(dpg.mvThemeCol_Text, [255, 255, 255, 255])       # Texto blanco
            dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5) # Bordes ligeramente más redondeados
            dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 10, 5) # Más padding interno

    # --- Ventana Principal de la Aplicación --- 
    with dpg.window(label="Web Scraper & PostgreSQL App", tag="main_window", width=800, height=600):
        dpg.add_text("Ingresa la URL a raspar:")
        dpg.add_input_text(tag="url_input", hint="Ej: https://www.ejemplo.com/noticias", width=-1) # Campo para la URL 
        dpg.add_spacer(height=10)
    
        # --- Centrar los botones ---
        with dpg.group(horizontal=True, width=0): # width=0 para que el grupo no ocupe todo el ancho
            # El spacer debe estar dentro del grupo de centrado y usa la variable calculada
            dpg.add_spacer(width=spacer_width_for_centering)   # Este spacer empuja los botones hacia el centro.

            # --- Botones en una fila horizontal ---
            with dpg.group(horizontal=True):
                dpg.add_button(label="Scrapear y Guardar Datos", callback=boton_scrapear_callback, tag="scrape_button") # Botó para iniciar scraping
                dpg.add_spacer(width=8) 
                dpg.add_button(label="Ver URLs Guardadas", callback=boton_ver_urls_callback, tag="view_urls_button") # Botó para ver URLs
                dpg.add_spacer(width=8)
                dpg.add_button(label="Limpiar Resultados y URL", callback=boton_limpiar_gui_callback, tag="clear_button") # Botó para limpiar GUI
            
        # --- Aplicar el tema a los botones ---
        dpg.bind_item_theme("scrape_button", "llamative_button_theme")
        dpg.bind_item_theme("view_urls_button", "llamative_button_theme")
        dpg.bind_item_theme("clear_button", "llamative_button_theme")
                                                 
        dpg.add_spacer(height=20)
        dpg.add_separator()
        dpg.add_text("Estado:", color=[200,200,200], tag="estado_label")
        dpg.add_text("Esperando URL...", tag="estado_text", wrap=0) # Área de mensajes 
        dpg.add_separator()
        dpg.add_spacer(height=10)

        dpg.add_text("Resultados del Scraping:", color=[200,200,200])
        # Área de visualización de resultados 
        # Usamos un grupo expandible para organizar los resultados
        with dpg.child_window(tag="resultados_group", autosize_x=True, autosize_y=True, border=True):
            dpg.add_text("Los resultados aparecerán aquí.", tag="placeholder_resultados")
            
    dpg.set_primary_window("main_window", True)
    
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()
# jose Linares C.I:27.952.174

# --- Importaciones: ---

import dearpygui.dearpygui as dpg 
import requests 
import json 

# --- 1. Configuración API: ---

API_KEY = "0d6790d238d5faa0637d1f503b49b780" 

BASE_URL = "https://api.openweathermap.org/data/2.5/weather" 

# --- 2. Función para Consultar el Clima ---

def consultar_clima_callback(sender, app_data): 
    
    ciudad = dpg.get_value("leer_ciudad")

    dpg.set_value("mostrar_mensaje", "Cargando clima...") # mensajes para indicar que la consulta está en progreso

    if not ciudad:
        dpg.set_value("mostrar_mensaje", "Error: Por favor, introduce el nombre de una ciudad.") # Validar el campo de la ciudad que no este vacío, mostrar un error
        
        # Se limpia los campos de resultado anteriores si los hubiera
        dpg.set_value("mostrar_ciudad", "")
        dpg.set_value("mostrar_temperatura", "")
        dpg.set_value("mostrar_sensacion", "")
        dpg.set_value("mostrar_descripcion", "")
        dpg.set_value("mostrar_humedad", "")
        return

    # Parámetros para la solicitud a la API de OpenWeatherMap 
    params = {
        "q": ciudad,
        "appid": API_KEY,
        "units": "metric", # Para obtener la temperatura en grados Celsius 
        "lang": "es"       # Para obtener la descripción del clima en español 
    }

    # Se realiza la solicitud requests.get() a la API 
    try:
        response = requests.get(BASE_URL, params=params)
        
        response.raise_for_status() # Para detectar errores HTTP (códigos 4xx o 5xx) 

        data = response.json() # Convertir la respuesta a JSON 

        # Se extraen los datos relevantes de la respuesta 
        nombre_ciudad = data["name"]
        temperatura = data["main"]["temp"]
        sensacion_termica = data["main"]["feels_like"]
        descripcion = data["weather"][0]["description"].capitalize()
        humedad = data["main"]["humidity"]

        # Se actualizan las etiquetas de texto en la GUI con los datos obtenidos 
        dpg.set_value("mostrar_ciudad", f"Ciudad: {nombre_ciudad}")
        dpg.set_value("mostrar_temperatura", f"Temperatura: {temperatura}°C")
        dpg.set_value("mostrar_sensacion", f"Sensación Térmica: {sensacion_termica}°C")
        dpg.set_value("mostrar_descripcion", f"Descripción: {descripcion}")
        dpg.set_value("mostrar_humedad", f"Humedad: {humedad}%")
        dpg.set_value("mostrar_mensaje", "Consulta exitosa.")
        
    # Se manejan posibles errores de conexión (red, DNS, etc.) o HTTP

    except requests.exceptions.RequestException as e: 
       
        dpg.set_value("mostrar_mensaje", f"Error de conexión: {e}. Verifica tu conexión a internet o la URL de la API.")
        
        # Se limpia los campos de resultado
        dpg.set_value("mostrar_ciudad", "")
        dpg.set_value("mostrar_temperatura", "")
        dpg.set_value("mostrar_sensacion", "")
        dpg.set_value("mostrar_descripcion", "")
        dpg.set_value("mostrar_humedad", "")
        
    except json.JSONDecodeError: # Manejo de errores si la respuesta no es JSON válido 
        
        dpg.set_value("mostrar_mensaje", "Error: Respuesta inválida de la API. Inténtalo de nuevo.")
        # Limpiamos los campos de resultado
        dpg.set_value("mostrar_ciudad", "")
        dpg.set_value("mostrar_temperatura", "")
        dpg.set_value("mostrar_sensacion", "")
        dpg.set_value("mostrar_descripcion", "")
        dpg.set_value("mostrar_humedad", "")
        
    except KeyError: # Manejo de errores si la estructura JSON es inesperada (ej. ciudad no encontrada)

        try:
            error_data = response.json()
            error_message = error_data.get("message", "Ciudad no encontrada o clave API inválida.")
            dpg.set_value("mostrar_mensaje", f"Error de la API: {error_message.capitalize()}")
        except:
            dpg.set_value("mostrar_mensaje", "Error: No se pudo procesar la respuesta. Posiblemente la ciudad no existe o hay un problema con la API.")
        # Limpiamos los campos de resultado
        dpg.set_value("mostrar_ciudad", "")
        dpg.set_value("mostrar_temperatura", "")
        dpg.set_value("mostrar_sensacion", "")
        dpg.set_value("mostrar_descripcion", "")
        dpg.set_value("mostrar_humedad", "")

# --- 3. Diseño de la Interfaz con DearPyGui ---
dpg.create_context() 

# Creación de la ventana del sistema operativo
dpg.create_viewport(title='Visualizacion del Clima con OpenWeatherMap', width=600, height=450) 
dpg.setup_dearpygui() 

# Ventana principal de la aplicación 
with dpg.window(label="Consulta el Clima De Tu Ciudad Favorita", tag="ventana_window"):
    dpg.add_text("Introduce el nombre de la ciudad:")
    
    # Campo de entrada de texto para leer ciudad 
    dpg.add_input_text(hint="Ej. San Diego", tag="leer_ciudad", width=250)
    
    dpg.add_spacing(height=10)
   
    dpg.add_button(label="Consultar Clima", callback=consultar_clima_callback) # Botón para consultar el clima con la función callback. 
    
    dpg.add_spacing(height=10)
    dpg.add_separator() # linea para hacer una separación visual
    dpg.add_spacing(height=10)

    # Área de mostrar los resultados 
    dpg.add_text("Datos del Clima:", color=[255, 165, 40]) # Naranja
    dpg.add_text("Ciudad: ", tag="mostrar_ciudad") 
    dpg.add_text("Temperatura: ", tag="mostrar_temperatura") 
    dpg.add_text("Sensación Térmica: ", tag="mostrar_sensacion")  
    dpg.add_text("Descripción: ", tag="mostrar_descripcion") 
    dpg.add_text("Humedad: ", tag="mostrar_humedad") 

    dpg.add_spacing(height=10)
    dpg.add_separator()
    dpg.add_spacing(height=5)

    # Área de mensajes y errores 
    dpg.add_text("Esperando consulta...", tag="mostrar_mensaje", color=[30, 150, 255]) # Azul claro 

# Aseguramos que la ventana principal siempre se muestre
dpg.set_primary_window("ventana_window", True)

dpg.show_viewport() 
dpg.start_dearpygui() 
dpg.destroy_context() 
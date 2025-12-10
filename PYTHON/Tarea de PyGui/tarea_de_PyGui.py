# jose linares. C.I: 27.952.174
# Calculadora de IMC con DearPyGui

import dearpygui.dearpygui as dpg        # Importa la librería DearPyGui 

def funcion_calcular_imc(sender, app_data, user_data): 
    """
    Función para calcular el IMC y mostrar el resultado.
    Se ejecuta cuando se presiona el botón "Calcular IMC".
    """
                                              
    peso = dpg.get_value("lee_peso")     # lee el valor del peso desde el campo de entrada del peso
   
    altura = dpg.get_value("lee_altura")   # lee el valor de la altura desde el campo de entrada de la altura


    if peso <= 0 or altura <= 0:     # valida el peso y la altura para que sean numeros positivos 
        
        dpg.set_value("resultado_imc", "Error: Ingresa valores mayores a 0 para el peso y altura.")
        return 

    imc = peso / (altura ** 2)

    categoria = ""     # Determina la categoría del IMC según los rangos establecidos
    if imc < 18.5:
        categoria = "Bajo peso"
    elif 18.5 <= imc < 25.0:
        categoria = "Peso normal"
    elif 25.0 <= imc < 30.0:
        categoria = "Sobrepeso"
    else:
        categoria = "Obesidad"

    dpg.set_value("resultado_imc", f"Tu IMC es {imc:.2f} (Categoría: {categoria})")  # Mensaje del resultado de la IMC con su categoría


dpg.create_context() # Enciende la librería y Crea el contexto de la interfaz cómo dibujar los botones, textos, campos de entrada, etc. el "cerebro" interno de DearPyGui

# Crea la ventana principal de la aplicación y sus elementos 
with dpg.window(label="Calculadora de IMC", width=500, height=400):
    
    dpg.add_text("Calculadora de Índice de Masa Corporal") # Título de la aplicación
    
    dpg.add_separator() # Linea para separar el titulo de los botones

    dpg.add_text("Peso (kg):") # Etiqueta para el campo del peso
    
    # Este es el cambo donde se ingresara el peso
    dpg.add_input_float(tag="lee_peso", default_value=0.0, width=240, format="%.2f")

    dpg.add_text("Altura (m):") # Etiqueta para el campo de la altura
    
    # Este es el cambo donde se ingresara la altura
    dpg.add_input_float(tag="lee_altura", default_value=0.0, width=240, format="%.2f")

    dpg.add_spacer(height=15) # Agrega un espacio vertical entre peso y altura

    # Botón para iniciar el cálculo del IMC, conectado a la función de calcular imc
    dpg.add_button(label="Calcular IMC", callback=funcion_calcular_imc)

    dpg.add_spacer(height=15) # Agrega otro espacio vertical

    # Campo de texto para mostrar el resultado del IMC y su categoría
    dpg.add_text(tag="resultado_imc", default_value="Introduce tus datos para calcular el IMC.")

# Configuración del viewport (ventana física del sistema operativo que permite mover, redimensionar, minimizar y cerrar.) el lienzo visible
dpg.create_viewport(title='Calculadora de IMC', width=550, height=450)

# Prepara DearPyGui para renderizar en el viewport (Conecta el "cerebro" con la "ventana")
dpg.setup_dearpygui()

# Muestra la ventana de la aplicación (Es el "Lanzador" para que el usuari lo vea en pantalla) pone en escena el programa
dpg.show_viewport()

# Inicia el bucle principal de DearPyGui. Es, en esencia, el "motor" que mantiene la aplicación viva, hasta que cierres la ventana
dpg.start_dearpygui()

# Para limpiar y liberar todos los recursos de DearPyGui (se cierra y apaga todo al cerrar la ventana) para liberar espacio en la memoria
dpg.destroy_context()
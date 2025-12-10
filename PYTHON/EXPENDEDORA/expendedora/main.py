print("Hola mundo") 
import dearpygui.dearpygui as dpg
import json
# Diccionario de productos
productos = {
    "A1": {"nombre": "Soda", "precio": 1.50},
    "A2": {"nombre": "Chips", "precio": 1.00},
    "A3": {"nombre": "Candy", "precio": 0.75},
    "B1": {"nombre": "Agua", "precio": 1.00},
    "B2": {"nombre": "Jugo", "precio": 1.25},
}
# La función guardar_compra guarda una compra en un archivo JSON
# llamado "compras.json".
# Recibe tres parámetros: codigo (código del producto), dinero_recibido (monto recibido)
# y vuelto (cambio).
# La función crea un diccionario 'compra' con estos detalles
# y luego lo agrega a la lista de compras en el archivo JSON.
# Si el archivo no existe o está vacío, crea una lista nueva.
def guardar_compra(codigo, dinero_recibido, vuelto):
    compra = {
        "codigo": codigo,
        "producto": productos[codigo]["nombre"],
        "precio": productos[codigo]["precio"],
        "dinero_recibido": dinero_recibido,
        "vuelto": vuelto
    }
    try:
        with open("compras.json", "r") as file:
            compras = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        compras = [] # Si el archivo no existe o está vacío, inicializa una lista vacía
    compras.append(compra)
    with open("compras.json", "w") as file:
        json.dump(compras, file, indent=4)
# La función comprar maneja la transacción de compra. Funciona así:
# 1. Obtiene el código del producto ("codigo_input") y la cantidad recibida
#    ("dinero_input") de los campos de entrada.
# 2. Verifica si el código del producto existe en el diccionario 'productos'.
# 3. Si el producto existe, verifica si la cantidad recibida es suficiente
#    para cubrir el precio del producto.
# 4. Si es suficiente, calcula el cambio (vuelto) y actualiza el campo de
#    resultado con un mensaje de éxito.
# 5. Llama a la función guardar_compra para guardar los detalles.
# 6. Si es insuficiente o el producto no se encuentra, actualiza el campo de
#    resultado con un mensaje de error.
# En resumen, esta función procesa una transacción de compra y actualiza
# la interfaz gráfica en consecuencia.
def comprar(sender, app_data, user_data):
    codigo = dpg.get_value("codigo_input")
    dinero_recibido_str = dpg.get_value("dinero_input")
    try:
        dinero_recibido = float(dinero_recibido_str)
    except ValueError:
        dpg.set_value("resultado", "Error: Ingresa un monto válido para el dinero recibido.")
        return
    if codigo in productos:
        producto = productos[codigo]
        precio_producto = float(producto["precio"]) # Asegura que el precio sea flotante
        if dinero_recibido >= precio_producto:
            vuelto = dinero_recibido - precio_producto
            dpg.set_value("resultado", f"Compraste {producto['nombre']} por ${precio_producto:.2f}. Vuelto: ${vuelto:.2f}")
            guardar_compra(codigo, dinero_recibido, vuelto)
        else:
            dpg.set_value("resultado", "Dinero insuficiente")
    else:
        dpg.set_value("resultado", "Producto no encontrado")
# Este fragmento de código es una función que muestra una lista de
# compras en una ventana de interfaz gráfica.
# Lee los datos de compra desde un archivo JSON llamado "compras.json",
# calcula totales de ventas, dinero recibido y cambio, y muestra los
# datos en una tabla con encabezados y un pie que muestra los totales.
# Si no hay compras registradas, muestra un mensaje indicándolo.
def mostrar_compras(sender, app_data, user_data):
    total_vendido = 0.0
    total_recibido = 0.0
    total_devuelto = 0.0
    try:
        with open("compras.json", "r") as file:
            compras = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        compras = [] # Si el archivo no existe o está corrupto, la lista de compras está vacía
    # La ventana de compras se crea cada vez que se llama a la función
    # Esto es una forma simple para el ejercicio, en aplicaciones complejas se podría gestionar de otra forma
    with dpg.window(label="Listado de Compras", width=600, height=350, pos=(610,0)):
        if compras:
            with dpg.table(header_row=True):
                dpg.add_table_column(label="Código")
                dpg.add_table_column(label="Producto")
                dpg.add_table_column(label="Precio")
                dpg.add_table_column(label="Dinero Recibido")
                dpg.add_table_column(label="Vuelto")
                for compra in compras:
                    with dpg.table_row():
                        dpg.add_text(compra["codigo"])
                        dpg.add_text(compra["producto"])
                        dpg.add_text(f"${float(compra['precio']):.2f}")
                        dpg.add_text(f"${float(compra['dinero_recibido']):.2f}")
                        dpg.add_text(f"${float(compra['vuelto']):.2f}")
                        total_vendido += float(compra['precio'])
                        total_recibido += float(compra['dinero_recibido'])
                        total_devuelto += float(compra['vuelto'])
            dpg.add_separator() # Separador antes del pie de tabla
            # Pie de tabla para mostrar los totales
            with dpg.table(header_row=False):
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                dpg.add_table_column()
                with dpg.table_row():
                    dpg.add_text("Total")
                    dpg.add_text("") # Columna vacía
                    dpg.add_text(f"${total_vendido:.2f}")
                    dpg.add_text(f"${total_recibido:.2f}")
                    dpg.add_text(f"${total_devuelto:.2f}")
            dpg.add_separator() # Separador después del pie de tabla
            dpg.add_text(f"Total Vendido: ${total_vendido:.2f}")
            dpg.add_text(f"Total Recibido: ${total_recibido:.2f}")
            dpg.add_text(f"Total Devuelto: ${total_devuelto:.2f}")
        else:
            dpg.add_text("No hay compras registradas.")
# Inicia el contexto de la interfaz gráfica y crea la ventana principal.
dpg.create_context()
with dpg.window(label="Máquina Expendedora", width=600, height=350):
    # Crea un cuadro de texto con un mensaje "Productos Disponibles".
    dpg.add_text("Productos Disponibles:")
    # Crea una tabla con los datos de los productos.
    with dpg.table(header_row=True):
        # Crea las columnas de la tabla.
        dpg.add_table_column(label="Código")
        dpg.add_table_column(label="Producto")
        dpg.add_table_column(label="Precio")
        # Crea las filas de la tabla.
        for codigo, info in productos.items():
            with dpg.table_row():
                dpg.add_text(codigo)
                dpg.add_text(info["nombre"])
                dpg.add_text(f"${info['precio']:.2f}")
    # Crea una línea separadora.
    dpg.add_separator()
    dpg.add_text("Datos de la compra")
    # Crea un grupo horizontal para los campos de entrada.
    with dpg.group(horizontal=True):
        # Crea un cuadro con bordes
        with dpg.child_window(height=40, width=280, border=True):
            # Crea dos campos de entrada para el código y el monto
            # recibido, en un grupo horizontal para mejorar la apariencia.
            with dpg.group(horizontal=True):
                # Crea un campo de entrada para el código del producto.
                dpg.add_text("Código", tag="codigo_label")
                dpg.add_input_text(tag="codigo_input", default_value="", width=50)
        # Crea un cuadro con bordes
        with dpg.child_window(height=40, width=280, border=True):
            # Crea otro grupo horizontal para mejorar la apariencia.
            with dpg.group(horizontal=True):
                # Crea dos campos de entrada para el monto recibido.
                dpg.add_text("Dinero recibido")
                dpg.add_input_text(tag="dinero_input", default_value="", decimal=True, width=100)
    # Crea un grupo horizontal para los botones.
    with dpg.group(horizontal=True):
        # Crea un tema para cada botón.
        with dpg.theme(tag="tema_boton_comprar"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (255, 0, 0, 128))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (255, 0, 0, 50))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (255, 0, 0, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)
        with dpg.theme(tag="tema_boton_mostrar"):
            with dpg.theme_component(dpg.mvButton):
                dpg.add_theme_color(dpg.mvThemeCol_Button, (0, 255, 0, 128))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonActive, (0, 255, 0, 50))
                dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (0, 255, 0, 255))
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 5)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 3, 3)
                dpg.add_theme_color(dpg.mvThemeCol_Text, [0, 0, 0, 255])
        # Crea el botón de comprar.
        dpg.add_button(label="Comprar", callback=comprar)
        # Asigna el tema al botón de comprar.
        dpg.bind_item_theme(dpg.last_item(), "tema_boton_comprar")
        # Crea el botón de mostrar compras.
        dpg.add_button(label="Mostrar Compras", callback=mostrar_compras)
        # Asigna el tema al botón de mostrar compras.
        dpg.bind_item_theme(dpg.last_item(), "tema_boton_mostrar")
    # Crea un cuadro de texto para mostrar el resultado de la compra.
    dpg.add_text(tag="resultado", default_value="", color=[255, 0, 0])
# Crea la ventana principal (viewport).
dpg.create_viewport(title="Máquina Expendedora", width=600, height=500)
# dpg.setup_dearpygui() es una función de inicialización de DearPyGui que se utiliza
# para configurar el entorno de DearPyGui antes de utilizar cualquier otro componente
# o función. Se utiliza para inicializar la biblioteca DearPyGui y
# asegurarse de que todo esté listo para ser utilizado. También se encarga de
# crear una ventana de interfaz gráfica y establecer la configuración de la ventana.
# Es importante llamar a dpg.setup_dearpygui() antes de utilizar cualquier otro
# componente o función de DearPyGui, ya que de lo contrario, es posible que no se
# muestren los elementos de la interfaz gráfica correctamente.
dpg.setup_dearpygui()
# Establece que la ventana principal estará maximizada en la pantalla.
dpg.maximize_viewport()
# Muestra la ventana principal.
dpg.show_viewport()
# Inicia el bucle de eventos de DearPyGui. Cuando se llama a dpg.start_dearpygui(),
# DearPyGui comienza a procesar eventos y a actualizar la interfaz gráfica de la
# aplicación. Esto incluye:
# - Procesar eventos de teclado y mouse.
# - Actualizar la posición y el tamaño de los elementos de la interfaz gráfica.
# - Dibujar la interfaz gráfica en la pantalla.
# - Procesar mensajes y eventos de la aplicación.
# En otras palabras, dpg.start_dearpygui() es el punto de partida para que la
# aplicación comience a funcionar y a interactuar con el usuario. Es importante
# tener en cuenta que dpg.start_dearpygui() es un bucle infinito, lo que significa
# que la aplicación se quedará ejecutando hasta que se cierre manualmente.
dpg.start_dearpygui()
# Destruye el contexto de DearPyGui. Es importante llamar a dpg.destroy_context() antes
# de salir de la aplicación para liberar los recursos utilizados por DearPyGui.
dpg.destroy_context()

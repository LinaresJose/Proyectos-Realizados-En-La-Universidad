# --- Actividad Práctica: Perfil de Usuario y Estadísticas Simples ---
# Objetivo: Desarrollar un programa de consola que recopile información de un usuario,
# procese algunos datos y muestre un resumen.

print("¡Bienvenido al creador de perfil de usuario!")
print("-" * 40) # Línea divisoria para mejor legibilidad

# --- 1. Recopilación de Datos Personales (Usando tipos básicos y conversión) ---

# Nombre (str): Almacena la entrada directamente, ya que input() devuelve una cadena.
nombre = input("Por favor, ingresa tu nombre: ")

# Edad (int): Se necesita conversión a entero. Usamos un bucle y try-except para validar la entrada.
while True:
    try:
        edad_str = input("Ingresa tu edad: ")
        edad = int(edad_str)
        if edad <= 0: # Asegurarse de que la edad sea un número positivo
            print("La edad debe ser un número positivo. Inténtalo de nuevo.")
            continue
        break # Si la conversión es exitosa y la edad es válida, salimos del bucle
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número entero para la edad.")

# Altura (float): Se necesita conversión a flotante. Usamos un bucle y try-except para validar.
while True:
    try:
        altura_str = input("Ingresa tu altura en metros (ej. 1.75): ")
        altura = float(altura_str)
        if not (0.5 <= altura <= 2.5): # Rango razonable para la altura
            print("La altura parece inusual. Por favor, ingresa un valor realista en metros.")
            continue
        break
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número (usando punto decimal) para la altura.")

# Peso (float): Necesario para el cálculo del IMC. Similar a la altura.
while True:
    try:
        peso_str = input("Ingresa tu peso en kilogramos (ej. 70.5): ")
        peso = float(peso_str)
        if not (20 <= peso <= 300): # Rango razonable para el peso
            print("El peso parece inusual. Por favor, ingresa un valor realista en kilogramos.")
            continue
        break
    except ValueError:
        print("Entrada inválida. Por favor, ingresa un número (usando punto decimal) para el peso.")

# Licencia de conducir (bool): Convierte "si"/"no" a True/False.
while True:
    licencia_str = input("¿Tienes licencia de conducir? (si/no): ").lower().strip()
    if licencia_str == "si":
        tiene_licencia = True
        break
    elif licencia_str == "no":
        tiene_licencia = False
        break
    else:
        print("Respuesta inválida. Por favor, escribe 'si' o 'no'.")

print("\n¡Genial! Ahora cuéntame más sobre ti.")

# --- 2. Recopilación de Hobbies (Usando Listas) ---
# Una lista es mutable, lo que nos permite añadir elementos dinámicamente.
hobbies = []
print("\nAhora cuéntame tus hobbies (escribe 'fin' o 'listo' cuando termines):")
while True:
    hobby = input(f"Hobby {len(hobbies) + 1}: ").strip()
    if hobby.lower() in ["fin", "listo"]:
        break
    if hobby: # Asegurarse de que no se añadan cadenas vacías
        hobbies.append(hobby)
    else:
        print("No ingresaste un hobby. Intenta de nuevo o escribe 'fin'.")

# --- 3. Ciudades Visitadas Recientemente (Usando Tuplas) ---
# Una tupla es inmutable, lo que significa que una vez creada, sus elementos no pueden cambiar.
# Aquí la creamos a partir de una lista temporal para la entrada.
ciudades_temp = []
print("\nAhora, las 3 últimas ciudades que visitaste:")
for i in range(3): # Pedimos exactamente 3 ciudades como en el ejemplo
    ciudad = input(f"Ciudad {i + 1}: ").strip()
    if ciudad:
        ciudades_temp.append(ciudad)
    else:
        print("No ingresaste una ciudad. Por favor, intenta de nuevo.")
        i -= 1 # Permite re-ingresar si la entrada fue vacía
ciudades_visitadas = tuple(ciudades_temp) # Convertimos la lista a una tupla

# --- 4. Información de Contacto (Usando Diccionarios) ---
# Un diccionario almacena pares clave-valor, ideal para datos con etiquetas descriptivas.
info_contacto = {}
print("\nPara tu información de contacto:")
email = input("Ingresa tu email: ").strip()
if email: # Solo añadir si no está vacío
    info_contacto["email"] = email
telefono = input("Ingresa tu teléfono: ").strip()
if telefono: # Solo añadir si no está vacío
    info_contacto["telefono"] = telefono

# --- 5. Palabras Favoritas Únicas (Usando Conjuntos) ---
# Un conjunto almacena elementos únicos y no ordenados. Ideal para eliminar duplicados.
palabras_favoritas_str = input("\nFinalmente, ingresa algunas palabras que te gusten (separadas por comas, ej. 'paz, amor, vida'): ").strip()
# Dividimos la cadena por comas, limpiamos espacios y creamos un conjunto
palabras_favoritas = set()
if palabras_favoritas_str:
    # Usamos una comprensión de lista para limpiar cada palabra antes de añadirla al conjunto
    palabras_favoritas = {palabra.strip() for palabra in palabras_favoritas_str.split(',') if palabra.strip()}

print("\n" + "-" * 40)
print("--- Resumen de tu Perfil ---")
print("-" * 40)

# --- 6. Mostrar Resumen del Perfil y Estadísticas Simples (Usando f-strings) ---

print(f"Nombre: {nombre}")
print(f"Edad: {edad} años", end="") # end="" para no añadir un salto de línea
if edad >= 18:
    print(" (¡Eres un adulto!)")
else:
    print(" (Eres menor de edad)")

print(f"Altura: {altura:.2f} metros") # Formatear a 2 decimales
print(f"Peso: {peso:.2f} kg") # Formatear a 2 decimales
print(f"Licencia de conducir: {'Sí' if tiene_licencia else 'No'}")

# Cálculo y muestra del IMC
if altura > 0: # Evitar división por cero
    imc = peso / (altura * altura)
    print(f"IMC (Índice de Masa Corporal): {imc:.2f}")
else:
    print("No se pudo calcular el IMC (altura inválida).")


print(f"\nTus hobbies: {', '.join(hobbies)} (Total: {len(hobbies)})")

# Mostrar las ciudades visitadas. Usamos ', '.join() para unirlas en una cadena legible.
print(f"Ciudades visitadas: {', '.join(ciudades_visitadas)}")

print("\nContacto:")
if info_contacto:
    for clave, valor in info_contacto.items():
        print(f"  {clave.capitalize()}: {valor}")
else:
    print("  No se proporcionó información de contacto.")

print(f"\nTus palabras favoritas únicas: {palabras_favoritas} (Total: {len(palabras_favoritas)})")

print("-" * 40)
print("¡Gracias por usar el creador de perfil!")
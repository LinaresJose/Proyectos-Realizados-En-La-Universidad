package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// main es la función de entrada del programa.
func main() {
	reader := bufio.NewReader(os.Stdin) // Para leer la entrada del usuario

	fmt.Println("¡Bienvenido al creador de perfil de usuario!")

	// 1. Bienvenida y Recopilación de Datos Personales (Usando tipos básicos)
	// Nombre (string)
	fmt.Print("Por favor, ingresa tu nombre: ")
	nombre, _ := reader.ReadString('\n')
	nombre = strings.TrimSpace(nombre) // Eliminar el salto de línea al final

	// Edad (int)
	var edad int
	for { // Bucle para validar la entrada
		fmt.Print("Ingresa tu edad: ")
		entradaEdad, _ := reader.ReadString('\n')
		entradaEdad = strings.TrimSpace(entradaEdad)
		var err error
		edad, err = strconv.Atoi(entradaEdad) // Convertir string a int
		if err != nil {
			fmt.Println("Entrada inválida. Por favor, ingresa un número entero para la edad.")
		} else {
			break // Salir del bucle si la conversión es exitosa
		}
	}

	// Altura (float64)
	var altura float64
	for { // Bucle para validar la entrada
		fmt.Print("Ingresa tu altura en metros (ej. 1.75): ")
		entradaAltura, _ := reader.ReadString('\n')
		entradaAltura = strings.TrimSpace(entradaAltura)
		var err error
		altura, err = strconv.ParseFloat(entradaAltura, 64) // Convertir string a float64
		if err != nil {
			fmt.Println("Entrada inválida. Por favor, ingresa un número decimal para la altura.")
		} else {
			break // Salir del bucle si la conversión es exitosa
		}
	}

	// Licencia de conducir (bool)
	var tieneLicencia bool
	for { // Bucle para validar la entrada
		fmt.Print("¿Tienes licencia de conducir? (si/no): ")
		entradaLicencia, _ := reader.ReadString('\n')
		entradaLicencia = strings.TrimSpace(strings.ToLower(entradaLicencia))
		if entradaLicencia == "si" {
			tieneLicencia = true
			break
		} else if entradaLicencia == "no" {
			tieneLicencia = false
			break
		} else {
			fmt.Println("Entrada inválida. Por favor, escribe 'si' o 'no'.")
		}
	}

	fmt.Println("\n¡Genial! Ahora cuéntame tus hobbies (escribe 'fin' cuando termines):")

	// 2. Recopilación de Hobbies (Usando Slices - equivalente a Listas de Python)
	var hobbies []string // Un slice de strings para almacenar los hobbies
	for {
		fmt.Printf("Hobby %d: ", len(hobbies)+1)
		hobby, _ := reader.ReadString('\n')
		hobby = strings.TrimSpace(hobby)
		if strings.ToLower(hobby) == "fin" {
			break
		}
		hobbies = append(hobbies, hobby) // Añadir el hobby al slice
	}

	fmt.Println("\nAhora, las ciudades que visitaste recientemente (ingresa una por una, presiona Enter para continuar y 'fin' para terminar):")

	// 3. Ciudades Visitadas Recientemente (Usando Slices, luego convertimos a Array si el tamaño es fijo)
	// Go no tiene tuplas en el mismo sentido que Python. Para una colección de elementos fijos e inmutables,
	// podemos usar un array (si el tamaño es conocido) o un slice que tratamos como inmutable después de la inicialización.
	// En este caso, como no se pide exactamente 3, un slice es más flexible.
	var ciudadesVisitadasSlice []string
	for {
		fmt.Printf("Ciudad %d: ", len(ciudadesVisitadasSlice)+1)
		ciudad, _ := reader.ReadString('\n')
		ciudad = strings.TrimSpace(ciudad)
		if strings.ToLower(ciudad) == "fin" {
			break
		}
		ciudadesVisitadasSlice = append(ciudadesVisitadasSlice, ciudad)
	}
	// Si quisiéramos una "tupla" de tamaño fijo, podríamos copiar a un array después de recopilar las 3 primeras:
	// var ciudadesVisitadas [3]string
	// if len(ciudadesVisitadasSlice) >= 3 {
	// 	copy(ciudadesVisitadas[:], ciudadesVisitadasSlice[:3])
	// } else {
	// 	copy(ciudadesVisitadas[:], ciudadesVisitadasSlice)
	// }

	fmt.Println("\nPara tu información de contacto:")

	// 4. Información de Contacto (Usando Mapas - equivalente a Diccionarios de Python)
	contacto := make(map[string]string) // Un mapa para almacenar clave-valor de string a string

	fmt.Print("Ingresa tu email: ")
	email, _ := reader.ReadString('\n')
	contacto["email"] = strings.TrimSpace(email)

	fmt.Print("Ingresa tu teléfono: ")
	telefono, _ := reader.ReadString('\n')
	contacto["telefono"] = strings.TrimSpace(telefono)

	fmt.Println("\nFinalmente, ingresa algunas palabras que te gusten (separadas por comas, ej. 'paz, amor, vida'):")

	// 5. Palabras Favoritas Únicas (Usando Mapas como Conjunto - equivalente a Conjuntos de Python)
	// Go no tiene un tipo de dato 'set' nativo. La forma idiomática de simular un conjunto
	// es usar un mapa donde las claves son los elementos únicos y los valores son un struct{} vacío
	// (que no ocupa espacio en memoria) para indicar la presencia.
	palabrasFavoritasUnicas := make(map[string]struct{}) // Simula un conjunto

	entradaPalabras, _ := reader.ReadString('\n')
	palabras := strings.Split(strings.TrimSpace(entradaPalabras), ",")
	for _, palabra := range palabras {
		palabraLimpia := strings.TrimSpace(palabra)
		if palabraLimpia != "" {
			palabrasFavoritasUnicas[palabraLimpia] = struct{}{} // Añadir al "conjunto"
		}
	}

	// 6. Resumen del Perfil y Estadísticas Simples
	fmt.Println("\n--- Resumen de tu Perfil ---")
	fmt.Printf("Nombre: %s\n", nombre)
	fmt.Printf("Edad: %d años", edad)
	if edad >= 18 {
		fmt.Println(" (¡Eres un adulto!)")
	} else {
		fmt.Println(" (Eres menor de edad)")
	}
	fmt.Printf("Altura: %.2f metros\n", altura)
	fmt.Printf("Licencia de conducir: %s\n", func() string {
		if tieneLicencia {
			return "Sí"
		}
		return "No"
	}()) // Función anónima para formatear el booleano

	fmt.Printf("Tus hobbies: %s (Total: %d)\n", strings.Join(hobbies, ", "), len(hobbies)) // strings.Join para formatear la lista
	fmt.Printf("Ciudades visitadas: %s\n", strings.Join(ciudadesVisitadasSlice, ", "))

	fmt.Println("Contacto:")
	fmt.Printf("  Email: %s\n", contacto["email"])
	fmt.Printf("  Teléfono: %s\n", contacto["telefono"])

	// Mostrar palabras favoritas únicas
	// Convertir el mapa de "conjunto" a un slice para mostrarlo ordenado (opcional)
	var palabrasUnicasSlice []string
	for palabra := range palabrasFavoritasUnicas {
		palabrasUnicasSlice = append(palabrasUnicasSlice, palabra)
	}
	// Opcional: Ordenar las palabras para una salida consistente
	// sort.Strings(palabrasUnicasSlice)
	fmt.Printf("Tus palabras favoritas únicas: %v (Total: %d)\n", palabrasUnicasSlice, len(palabrasFavoritasUnicas))

	// Calcular IMC (solicitar peso)
	var peso float64
	for {
		fmt.Print("Para calcular tu IMC, ingresa tu peso en kilogramos (opcional, deja en blanco y presiona Enter si no quieres): ")
		entradaPeso, _ := reader.ReadString('\n')
		entradaPeso = strings.TrimSpace(entradaPeso)
		if entradaPeso == "" {
			fmt.Println("IMC no calculado (peso no proporcionado).")
			break
		}
		var err error
		peso, err = strconv.ParseFloat(entradaPeso, 64)
		if err != nil {
			fmt.Println("Entrada inválida. Por favor, ingresa un número decimal para el peso.")
		} else if peso <= 0 {
			fmt.Println("El peso debe ser un valor positivo.")
		} else {
			imc := peso / (altura * altura)
			fmt.Printf("Tu IMC es: %.2f\n", imc)
			break
		}
	}
}

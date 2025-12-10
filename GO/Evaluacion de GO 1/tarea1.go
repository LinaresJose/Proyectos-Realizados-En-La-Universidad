package main

import "fmt"

func main() {
	var numero int
	var error error

	fmt.Print("\nPrograma para leer y verificar si un numero es par o impar \n")

	for {
		fmt.Print("\nIntroduce un número entero: ")
		_, error = fmt.Scan(&numero) // Lee la entrada del usuario y la almacena en la variable 'numero'.

		if error != nil {
			fmt.Println("\n¡Error! no es un número entero válido. Por favor, intenta de nuevo.")
			var limpiar string
			fmt.Scanln(&limpiar) // Lee el resto de la línea para descartar la entrada incorrecta.
			continue
		}
		break
	}

	if numero%2 == 0 {
		fmt.Printf("\nEl numero %d es par", numero)
	} else {
		fmt.Printf("\nEl numero %d es impar", numero)
	}

}

package main

import "fmt"

func main() {

	var numero1, numero2, numero3, numero4, numero5 float64

	fmt.Print("\nPrograma para leer 5 numeros, calcular el promedio y mostrar cual es mayor y menor \n")

	fmt.Print("\nIngrese el primer numero: ")
	fmt.Scan(&numero1)
	fmt.Print("\nIngrese el segundo numero: ")
	fmt.Scan(&numero2)
	fmt.Print("\nIngrese el tercer numero: ")
	fmt.Scan(&numero3)
	fmt.Print("\nIngrese el cuarto numero: ")
	fmt.Scan(&numero4)
	fmt.Print("\nIngrese el quinto numero: ")
	fmt.Scan(&numero5)

	suma := numero1 + numero2 + numero3 + numero4 + numero5
	promedio := suma / 5
	fmt.Printf("\nEl promedio es: %.2f\n", promedio)

	mayor := numero1
	menor := numero1

	if numero2 > mayor {
		mayor = numero2
	}
	if numero2 < menor {
		menor = numero2
	}
	if numero3 > mayor {
		mayor = numero3
	}
	if numero3 < menor {
		menor = numero3
	}
	if numero4 > mayor {
		mayor = numero4
	}
	if numero4 < menor {
		menor = numero4
	}
	if numero5 > mayor {
		mayor = numero5
	}
	if numero5 < menor {
		menor = numero5
	}
	fmt.Printf("\nEl número mayor es: %.2f\n", mayor)
	fmt.Printf("\nEl número menor es: %.2f\n", menor)
}

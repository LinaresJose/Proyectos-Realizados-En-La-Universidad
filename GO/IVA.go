package main

import (
	// Necesario para leer líneas con espacios
	"fmt" // Para imprimir y leer
)

//func main() {
	// Usamos Println para imprimir una línea de texto
	fmt.Println("--- Calculadora de IVA en Go ---")

	fmt.Print("Ingrese su nombre: ")
	var nombre string
	fmt.Scanln(&nombre)

	fmt.Print("Ingrese Monto: ")
	var monto float64
	fmt.Scanln(&monto)

	var iva float64 = monto * 0.16
	var total float64 = monto + iva

	fmt.Println("--- Resultados ---")
	fmt.Println("Nombre:", nombre)
	fmt.Println("Base Imponible:$", monto)
	fmt.Println("IVA:$", iva)
	fmt.Println("Total a Pagar:$", total)
	fmt.Println("--------------------")
	fmt.Println("¡Programa finalizado!")

}

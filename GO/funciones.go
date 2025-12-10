package main

import (
	"fmt"
	"strings"
)

func hola() {
	fmt.Print("\nhola mundo\n")
}

func sumar(A int64, B int64) {
	var SUMA int64
	SUMA = A + B
	fmt.Printf("\nla suma es %d\n", SUMA)
}

func mayor_menor(A int64, B int64) {
	mayor := A
	menor := A

	if B > mayor {
		mayor = B
		fmt.Printf("\nEl numero mayor es %d\n", mayor)
	}

	if B < menor {
		menor = B
		fmt.Printf("\nEl numero menor es %d\n", menor)
	}

}

func mayuscula(palabra string) {
	var conver string
	conver = strings.ToUpper(palabra)
	fmt.Print("\nla palabra se puso en mayuscula: ", conver)

}

func main() {

	var palabra string
	var A int64
	var B int64
	hola()

	fmt.Print("\nIntroduce una palabra: ")
	fmt.Scan(&palabra)
	mayuscula(palabra)

	fmt.Print("\nIntroduce el primer número entero: ")
	fmt.Scan(&A)
	fmt.Print("\nIntroduce el segundo número entero: ")
	fmt.Scan(&B)

	sumar(A, B)
	mayor_menor(A, B)
}

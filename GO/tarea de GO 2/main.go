package main

import "fmt"

func calcular_bono(ventas float64) {

	var porcentaje float64
	var monto_bonificacion float64

	if ventas >= 1000000 && ventas < 3000000 {

		porcentaje = 0.04

	} else if ventas >= 3000000 && ventas < 5000000 {

		porcentaje = 0.05

	} else if ventas >= 5000000 && ventas < 7000000 {

		porcentaje = 0.06

	} else if ventas >= 7000000 {

		porcentaje = 0.07
	} else {
		porcentaje = 0.0
	}

	monto_bonificacion = ventas * porcentaje

	porcentaje_bono := porcentaje * 100

	fmt.Printf("\nTienes un bono del %.f%%.\n ", porcentaje_bono)
	fmt.Printf("\nSu bonificacion es: %.2f BS", monto_bonificacion)

}

func main() {

	var nombre string
	fmt.Print("\nIngrese su nombre: ")
	fmt.Scan(&nombre)

	var apellido string
	fmt.Print("\nIngrese su apellido: ")
	fmt.Scan(&apellido)

	var ventas float64
	fmt.Print("\nIngrese el monto de las ventas: ")
	fmt.Scan(&ventas)

	fmt.Printf("\nEl empleado %s %s Vendio un total de: %0.2f BS\n ", nombre, apellido, ventas)

	calcular_bono(ventas)

}

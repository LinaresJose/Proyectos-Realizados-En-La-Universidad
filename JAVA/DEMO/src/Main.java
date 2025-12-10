import java.util.Scanner;

public class Main {
    public static void main(String[] args) {

        Scanner scanear=new Scanner(System.in);

        int cantidad_de_notas=0;

        double suma_notas=0;

        double nota_maxima=-1;

        double promedio=0;

        boolean cantidadValida = false;

        do {
            System.out.print("¿Cuántas notas desea ingresar (debe ser un número entero positivo)?: ");

            if (scanear.hasNextInt()) {
                cantidad_de_notas = scanear.nextInt();

                if (cantidad_de_notas > 0) {
                    cantidadValida = true; // La condición se cumple, salimos del bucle
                } else {
                    System.out.println("Error: La cantidad de notas debe ser un número mayor que cero.");
                }
            } else {
                // Error: No es un número entero.
                System.out.println("Error: Solo se permiten números enteros para la cantidad de notas.");
                scanear.next(); // Limpiar el token no numérico
            }
        } while (!cantidadValida);

        cantidad_de_notas=scanear.nextInt();

        for (int i = 1; i <=cantidad_de_notas ; i++) {

            double nota=0;
            boolean nota_invalida=false;

            while (!nota_invalida){

                System.out.print("Ingrese la nota #"+ i + " (0 al 20):");

                if (scanear.hasNextDouble()){
                    nota=scanear.nextDouble();
                    if (nota >= 0 && nota <21){
                        nota_invalida=true;
                    }else {
                        System.out.println("Error: La nota debe estar entre 0 y 20.");
                        scanear.next();
                    }
                }
            }
            suma_notas += nota;
            if (nota >= nota_maxima) {
                nota_maxima=nota;
            }
        }
        scanear.close();
        promedio=suma_notas/cantidad_de_notas;

        System.out.printf("el promedio de %d notas es: %.2f y la nota Maxima fue: %.2f",cantidad_de_notas,promedio,nota_maxima);
    }
}
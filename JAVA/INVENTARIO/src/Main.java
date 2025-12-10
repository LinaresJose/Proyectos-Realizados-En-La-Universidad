import java.util.Scanner;

//TIP Para <b>ejecutar</b> el código, pulsar <shortcut actionId="Run"/> o
// Haz clic en el ícono <icon src="AllIcons.Actions.Execute"/> del margen.
public class Main {
    public static void main(String[] args) {

        System.out.println("Registro y Análisis básico de precios de productos en un inventario.");

        Scanner leer=new Scanner(System.in);

        int cantidad_de_producto=0;

        System.out.println("Ingresa el numero de productos que deseas registrar");

        cantidad_de_producto=leer.nextInt();
        leer.nextLine();

        // declaramos un arreglo para almacenar los nombres y precios de los productos

        String [] nombres;
        nombres=new String[cantidad_de_producto];

        float [] precios;
        precios=new float[cantidad_de_producto];

        // una variable acumulativa para el total de los precios
        float suma_total_precios=0.00f;

        // registramos el numero de productos con un ciclo for

        for (int i = 0; i < cantidad_de_producto; i++) {

            System.out.println("Ingrese el nombre del producto #"+(i+1)+": ");
            nombres[i]= leer.nextLine();

            //declaramos una variable para validar el precio entre 1 y 1.000
            // y un boolean para repetir el ciclo hasta que sea verdadero

            float verificacion_precio=0.00f;
            boolean precio_correcto=false;

            while (precio_correcto == false) {
                System.out.println("Ingrese el precio del producto #" + (i+1) + ": ");
                verificacion_precio = leer.nextFloat();

                if (verificacion_precio >= 1.00f && verificacion_precio <= 1000.00f) {

                    System.out.println("Precio guardado exitosamente");
                    precios[i] = verificacion_precio;
                    precio_correcto=true;
                    suma_total_precios += precios[i];

                } else {
                    System.out.println("El presio debe de ser entre 1.00 y 1000.00");
                }
                leer.nextLine();
            }
        }
        // declaramos variables para calcular El Precio Promedio de todos los productos.
        float promedio=suma_total_precios/cantidad_de_producto;

        // Declaramos variables para encontrar el precio más alto y el precio más bajo registrados
        float precio_mas_alto=precios[0];
        float precio_mas_bajo=precios[0];

        // Declaramos una variables para saber cuantos productos tienen precion primiun
        int productos_Premium=0;

        // realizamos un ciclo for para verificar los precios max y min. segun la cantidad de productos
        for (int i = 0; i < cantidad_de_producto ; i++) {

            if (precios[i]>precio_mas_alto){
                precio_mas_alto=precios[i];
            }
            if (precios[i]<precio_mas_bajo){
                precio_mas_bajo=precios[i];
           }
            if (precios[i]>500){
                productos_Premium++;
            }

        }
        System.out.println("\n--- LISTA DE PRODUCTOS REGISTRADOS ---");
        System.out.println("No. | Producto | Precio");
        System.out.println("-------------------------------------");

        for (int i = 0; i < cantidad_de_producto ; i++) {
            //%-3d: Imprime un número entero (d) alineado a la izquierda (-) en un espacio de 3 caracteres.
            //%-20s: Imprime una cadena de texto (s) alineada a la izquierda (-) en un espacio de 20 caracteres (útil para que los nombres no se amontonen
            System.out.printf("%-3d | %-20s | $%.2f\n",(i+1),nombres[i],precios[i]);
        }
        System.out.println("-------------------------------------");
        // Mostrar el resultado con formato a 2 decimales
        System.out.println("\n--- ANÁLISIS DE PRECIOS ---\n");
        System.out.printf("La suma total de los precios es: %.2f\n",suma_total_precios);
        System.out.printf("El Precio Promedio de los productos es: %.2f\n", promedio);
        System.out.printf("El Precio Más Alto registrado es: %.2f\n", precio_mas_alto);
        System.out.printf("El Precio Más Bajo registrado es: %.2f\n", precio_mas_bajo);
        System.out.printf("Cantidad de productos 'Premium' (Precio > $500.00): %d\n",productos_Premium);
    }
}
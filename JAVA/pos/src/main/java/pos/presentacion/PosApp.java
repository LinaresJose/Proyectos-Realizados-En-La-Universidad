package pos.presentacion;

import pos.datos.IProductoDAO;
import pos.datos.ProductoDAO;
import pos.dominio.Producto;

import java.util.Scanner;

public class PosApp {

    private static IProductoDAO productoDAO = new ProductoDAO();
    private static Scanner consola = new Scanner(System.in);

    public static void main(String[] args) {
        ejecutarApp();
    }

    private static void ejecutarApp() {
        var salir = false;
        while (!salir) {
            try {
                var opcion = mostrarMenu();
                salir = ejecutarOpciones(opcion);
            } catch (Exception e) {
                System.out.println("Error: Ingresaste un valor no numérico o inválido. " + e.getMessage());
            }
            System.out.println();
        }
    }

    private static int mostrarMenu() {
        System.out.print("""
                
                *** Sistema POS - Gestión de Productos ***
                1. Listar Productos
                2. Buscar Producto por ID
                3. Agregar Producto
                4. Modificar Producto
                5. Eliminar Producto
                6. Salir
                Elije una opción: """);
        return Integer.parseInt(consola.nextLine());
    }

    private static boolean ejecutarOpciones(int opcion) {
        var salir = false;
        switch (opcion) {
            case 1 -> { // 1. Listar Productos (READ)
                System.out.println("--- Lista de Productos ---");
                var productos = productoDAO.listarProductos();
                productos.forEach(System.out::println);
            }
            case 2 -> { // 2. Buscar Producto por ID (READ)
                System.out.println("--- Buscar Producto ---");
                System.out.print("ID Producto: ");
                var idProducto = Integer.parseInt(consola.nextLine());
                var producto = new Producto(idProducto);
                var encontrado = productoDAO.buscarProductoPorId(producto);
                if (encontrado)
                    System.out.println("Producto encontrado: " + producto);
                else
                    System.out.println("Producto NO encontrado: " + idProducto);
            }
            case 3 -> { // 3. Agregar Producto (CREATE)
                System.out.println("--- Agregar Producto ---");
                var producto = solicitarDatosProducto(false); // Pedir datos sin ID
                var agregado = productoDAO.agregarProducto(producto);
                if (agregado)
                    System.out.println("Producto agregado exitosamente: " + producto);
                else
                    System.out.println("Producto NO agregado. Revise la conexión.");
            }
            case 4 -> { // 4. Modificar Producto (UPDATE)
                System.out.println("--- Modificar Producto ---");
                var producto = solicitarDatosProducto(true); // Pedir ID y datos
                var modificado = productoDAO.modificarProducto(producto);
                if (modificado)
                    System.out.println("Producto modificado exitosamente: " + producto);
                else
                    System.out.println("Producto NO modificado. Revise el ID o los datos.");
            }
            case 5 -> { // 5. Eliminar Producto (DELETE)
                System.out.println("--- Eliminar Producto ---");
                System.out.print("ID Producto a eliminar: ");
                var idProducto = Integer.parseInt(consola.nextLine());
                var producto = new Producto(idProducto);
                var eliminado = productoDAO.eliminarProducto(producto);
                if (eliminado)
                    System.out.println("Producto Eliminado: " + producto);
                else
                    System.out.println("Producto NO eliminado. Revise el ID.");
            }
            case 6 -> { // 6. Salir
                System.out.println("¡Gracias por usar el Sistema POS!");
                salir = true;
            }
            default -> System.out.println("Opción no válida: " + opcion);
        }
        return salir;
    }

    // Método auxiliar para pedir los datos del producto
    private static Producto solicitarDatosProducto(boolean requiereId) {
        int id = 0;
        if (requiereId) {
            System.out.print("ID Producto: ");
            id = Integer.parseInt(consola.nextLine());
        }
        System.out.print("Nombre: ");
        var nombre = consola.nextLine();
        System.out.print("Cantidad (Stock): ");
        var cantidad = Integer.parseInt(consola.nextLine());
        System.out.print("Precio: ");
        var precio = Double.parseDouble(consola.nextLine());
        System.out.print("Descripción: ");
        var descripcion = consola.nextLine();

        if (requiereId) {
            return new Producto(id, nombre, cantidad, precio, descripcion);
        } else {
            return new Producto(nombre, cantidad, precio, descripcion);
        }
    }

}
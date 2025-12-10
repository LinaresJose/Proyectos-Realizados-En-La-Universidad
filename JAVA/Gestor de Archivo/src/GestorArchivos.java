import java.io.*;
import java.util.Scanner; // Clase que usaremos para leer el contenido del archivo línea por línea

// Utilidades modernas para Copiar Archivos (java.nio.file, más robusto)
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;

public class GestorArchivos {

    // 1. Crear un archivo
    // ----------------------------------------------------
    public static void crearArchivo(String nombreArchivo) {

        System.out.println("\n--- 1. CREAR ARCHIVO ---");
        try {
            // Creamos una referencia lógica (objeto) al archivo en el sistema
            File archivo = new File(nombreArchivo);

            // Intentamos crear el archivo físicamente en el disco
            if (archivo.createNewFile()) {
                // Si devuelve true, el archivo fue creado
                System.out.println("✅ Éxito: Archivo creado: " + archivo.getName());
            } else {
                // Si devuelve false, el archivo ya existía
                System.out.println("ℹ️ Archivo ya existía.");
            }
            // Capturamos cualquier error de Entrada/Salida (ej.: falta de permisos)
        } catch (IOException e) {
            System.err.println("❌ Error al crear el archivo: " + e.getMessage());
        }
    }// ----------------------------------------------------

    // 2. Escribir en un archivo
    // El parámetro 'agregar' (true) añade contenido; (false) sobreescribe.
    // ----------------------------------------------------
    public static void escribirEnArchivo(String nombreArchivo, String contenido, boolean agregar) {

        System.out.println("\n--- 2. ESCRIBIR ARCHIVO ---");

        // try-with-resources: Asegura que el escritor se cierre automáticamente
        try (PrintWriter escritor = new PrintWriter(new FileWriter(nombreArchivo, agregar))) {

            // El 'FileWriter' se inicializa con 'agregar' para definir el modo de escritura
            // Escribimos la cadena de contenido y añadimos un salto de línea
            escritor.println(contenido);
            System.out.println("✍️ Éxito: Contenido escrito en " + nombreArchivo + ".");

            // Capturamos errores durante el proceso de escritura
        } catch (IOException e) {
            System.err.println("❌ Error al escribir en el archivo: " + e.getMessage());
        }
    }// ----------------------------------------------------

    // 3. Leer un archivo
    // ----------------------------------------------------
    public static void leerArchivo(String nombreArchivo) {

        System.out.println("\n--- 3. LEER ARCHIVO (" + nombreArchivo + ") ---");

        // try-with-resources: Crea un Scanner para leer el archivo y lo cierra al terminar
        try (Scanner lector = new Scanner(new File(nombreArchivo))) {

            // Bucle que se repite mientras haya líneas de texto para leer
            while (lector.hasNextLine()) {
                // Lee la línea completa y la guarda en la variable 'linea'
                String linea = lector.nextLine();
                System.out.println(">> " + linea);
            }
            // Captura el error específico si el archivo no existe
        } catch (FileNotFoundException e) {
            System.err.println("❌ Error: Archivo no encontrado. No se pudo leer.");
        }
    }// ----------------------------------------------------

    // 4. Copiar un archivo (Usando la librería moderna java.nio.file)
    // ----------------------------------------------------
    public static void copiarArchivo(String origen, String destino) {

        System.out.println("\n--- 4. COPIAR ARCHIVO ---");

        // Convierte la cadena de ruta del archivo de origen a un objeto Path
        Path archivoOrigen = Path.of(origen);
        // Convierte la cadena de ruta del archivo de destino a un objeto Path
        Path archivoDestino = Path.of(destino);

        try {
            // El método Files.copy realiza la operación de copia
            // StandardCopyOption.REPLACE_EXISTING: Opción para sobreescribir el destino si ya existe
            Files.copy(archivoOrigen, archivoDestino, StandardCopyOption.REPLACE_EXISTING);
            System.out.println("📄 Éxito: Archivo copiado de '" + origen + "' a '" + destino + "'.");
        } catch (IOException e) {
            // Captura errores si el archivo de origen no existe o hay problemas de I/O
            System.err.println("❌ Error al copiar el archivo. Revise que el origen exista: " + e.getMessage());
        }
    }// ----------------------------------------------------

    // 5. Eliminar un archivo
    // ----------------------------------------------------
    public static void eliminarArchivo(String nombreArchivo) {

        System.out.println("\n--- 5. ELIMINAR ARCHIVO ---");
        // Creamos la referencia al archivo a eliminar
        File archivo = new File(nombreArchivo);

        // Intentamos eliminar el archivo del sistema
        if (archivo.delete()) {
            // Si devuelve true, la eliminación fue exitosa
            System.out.println("🗑️ Éxito: Archivo eliminado: " + archivo.getName());
        } else {
            // Si devuelve false, el archivo no existía o el programa no tiene permisos
            System.err.println("❌ Error: No se pudo eliminar el archivo. Puede que no exista o esté en uso.");
        }
    }
}
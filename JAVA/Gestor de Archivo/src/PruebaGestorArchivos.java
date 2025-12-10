public class PruebaGestorArchivos {

    public static void main(String[] args) {

        String archivoPrincipal = "copia.txt";
        String archivoCopia = "registro_copia.txt";

        // 1. CREAR EL ARCHIVO principal
        //GestorArchivos.crearArchivo(archivoPrincipal);

        // 2. ESCRIBIR datos iniciales (false: sobreescribe)
       //GestorArchivos.escribirEnArchivo(archivoPrincipal,"HOLA mundo",false);

        // Añadir una línea (true: añade)
       //GestorArchivos.escribirEnArchivo(archivoPrincipal,"nuevo contenido",true);

        // 3. LEER el contenido actual
        //GestorArchivos.leerArchivo(archivoPrincipal);

        // 4. COPIAR el archivo principal al archivo de copia
        //GestorArchivos.copiarArchivo(archivoPrincipal,archivoCopia);


        // 5. ELIMINAR el archivo de copia
        //GestorArchivos.eliminarArchivo(archivoCopia);
    }

}
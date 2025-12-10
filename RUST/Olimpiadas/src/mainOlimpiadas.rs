use std::io;
use std::fs;

// 1. Declarar el módulo
mod procesamiento;

// Usamos el asterisco para traer todas las estructuras y funciones públicas
// del módulo 'procesamiento' al alcance de main.
use procesamiento::*; 

fn main() -> io::Result<()> {
    let archivo_entrada = "Calificación.txt";
    let archivo_salida = "Puntaje Final.txt";

    println!("--- Programa de Olimpiadas de Invierno ---");

    // 1. Lectura de datos usando el Subprograma 1
    let participantes_data = match leer_datos_calificacion(archivo_entrada) {
        Ok(data) => {
            println!("✅ Archivo de entrada leído y parseado exitosamente.");
            data
        },
        Err(e) => {
            eprintln!("❌ Error al leer el archivo {}: {}", archivo_entrada, e);
            eprintln!("Asegúrese de que el archivo existe y el formato es correcto.");
            return Err(e);
        }
    };
    
    let mut resultados_finales = Vec::new();

    // 2. Procesamiento de cada participante (usando Subprogramas 3, 4 y 5)
    for p_entrada in participantes_data {
        // Subprograma 3: Obtiene los puntajes totales de cada jurado
        let puntajes_totales = obtener_puntajes_totales_jurado(&p_entrada);
        
        // Subprograma 5: Calcula el promedio final (que usa el Subprograma 4 internamente)
        let puntaje_final = calcular_puntaje_final(&puntajes_totales);

        // Almacenar el resultado
        resultados_finales.push(ResultadoPatinador {
            nombre: p_entrada.nombre,
            puntajes_por_jurado: puntajes_totales,
            puntaje_final,
        });
    }
    
    println!("✅ Cálculos completados para {} participantes.", resultados_finales.len());

    // 3. Impresión al archivo de salida (Subprograma 6)
    imprimir_a_archivo(archivo_salida, &resultados_finales)?;

    println!("✅ Resultados escritos en '{}'", archivo_salida);
    
    // Mostrar la salida por consola para verificación
    println!("\n--- Contenido de Puntaje Final.txt ---");
    println!("{}", fs::read_to_string(archivo_salida)?);

    Ok(())
}

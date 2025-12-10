use std::fs::{self, File};
use std::io::{self, BufRead, BufReader, Write};
use std::fmt::Write as FmtWrite;

// --- ESTRUCTURAS DE DATOS ---

// Representa las calificaciones Artística y Técnica de un juez
#[derive(Debug)]
pub struct CalificacionJuez {
    pub artistica: f64, // 40%
    pub tecnica: f64,   // 60%
}

// Datos de entrada de un participante
pub struct ParticipanteEntrada {
    pub nombre: String,
    pub calificaciones: Vec<CalificacionJuez>,
}

// Estructura de salida
#[derive(Debug)]
pub struct ResultadoPatinador {
    pub nombre: String,
    pub puntajes_por_jurado: Vec<f64>, // Subprograma 3
    pub puntaje_final: f64,             // Subprograma 5
}


// --- SUBPROGRAMAS (LÓGICA) ---

// 1. Un subprograma que lea el archivo de datos "Calificación.txt"
pub fn leer_datos_calificacion(ruta: &str) -> io::Result<Vec<ParticipanteEntrada>> {
    let archivo = File::open(ruta)?;
    let reader = BufReader::new(archivo);
    let mut lineas = reader.lines().filter_map(Result::ok);
    let mut participantes = Vec::new();

    // La primera línea contiene el número de jurados (N)
    let n_jurados_line = lineas.next()
        .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidData, "Archivo vacío"))?;
    let n_jurados: u8 = n_jurados_line.trim().parse()
        .map_err(|_| io::Error::new(io::ErrorKind::InvalidData, "N no es un número válido"))?;

    // Procesar los datos de cada participante, asumiendo (Nombre, Calificaciones) en dos líneas.
    while let Some(linea_nombre) = lineas.next() {
        let linea_calif = lineas.next()
            .ok_or_else(|| io::Error::new(io::ErrorKind::InvalidData, "Falta línea de calificaciones"))?;

        // 1. Extraer el nombre (lo que está antes de la coma)
        let nombre = linea_nombre.trim_end_matches(',').trim().to_string();

        // 2. Parsear las calificaciones (asumiendo que están separadas por coma)
        let calif_vals: Vec<f64> = linea_calif.split(',')
            .filter_map(|s| s.trim().parse().ok())
            .collect();
        
        // 3. Crear los pares (Artístico, Técnico) para N jurados
        let mut calificaciones_juez = Vec::new();
        for i in 0..(n_jurados as usize) {
            let inicio_artistico = i * 2;
            let inicio_tecnico = i * 2 + 1;
            
            if inicio_tecnico < calif_vals.len() {
                calificaciones_juez.push(CalificacionJuez {
                    artistica: calif_vals[inicio_artistico],
                    tecnica: calif_vals[inicio_tecnico],
                });
            } else {
                 return Err(io::Error::new(io::ErrorKind::InvalidData, "Número incorrecto de calificaciones para los jueces"));
            }
        }

        participantes.push(ParticipanteEntrada { nombre, calificaciones: calificaciones_juez });
    }

    Ok(participantes)
}

// 2. Un subprograma que determine el puntaje total de UN jurado.
pub fn calcular_puntaje_jurado(calif: &CalificacionJuez) -> f64 {
    // 40% artístico y 60% técnico
    (calif.artistica * 0.40) + (calif.tecnica * 0.60)
}

// 3. Un subprograma que reciba los puntajes dados por cada jurado... y devuelva
//    en el arreglo que le parezca más conveniente los resultados totales de cada jurado.
pub fn obtener_puntajes_totales_jurado(participante: &ParticipanteEntrada) -> Vec<f64> {
    participante.calificaciones.iter()
        .map(calcular_puntaje_jurado)
        .collect()
}

// 4. Un subprograma que determine el puntaje mayor y menor dado por el jurado.
pub fn obtener_mayor_y_menor(puntajes: &[f64]) -> (f64, f64) {
    if puntajes.is_empty() {
        return (0.0, 0.0);
    }
    
    // El método .cloned() es necesario para obtener copias de los f64 (que implementan Copy)
    let max_puntaje = puntajes.iter().cloned().fold(f64::NEG_INFINITY, f64::max);
    let min_puntaje = puntajes.iter().cloned().fold(f64::INFINITY, f64::min);
    
    (max_puntaje, min_puntaje)
}

// 5. Un subprograma que obtenga el puntaje total obtenido por el equipo o patinador.
pub fn calcular_puntaje_final(puntajes_totales: &[f64]) -> f64 {
    let num_jurados = puntajes_totales.len();
    if num_jurados < 3 {
        // Se requieren al menos 3 puntajes para eliminar el mayor y el menor.
        return 0.0;
    }
    
    let (maximo, minimo) = obtener_mayor_y_menor(puntajes_totales);
    
    // Suma de todos los puntajes
    let suma_total: f64 = puntajes_totales.iter().sum();
    
    // Suma ajustada = Suma Total - Máximo - Mínimo
    let suma_ajustada = suma_total - maximo - minimo;
    
    // Divisor = N - 2
    let divisor = num_jurados as f64 - 2.0;
    
    suma_ajustada / divisor
}

// 6. Un subprograma que imprima al archivo de datos "Puntaje Fina.txt", los nombres de cada
//    patinador, el puntaje total otorgado por cada jurado y el puntaje total obtenido.
pub fn imprimir_a_archivo(ruta: &str, resultados: &[ResultadoPatinador]) -> io::Result<()> {
    let mut contenido = String::new();

    // Encabezado
    writeln!(&mut contenido, "Nombre | Puntajes Jurado (Totales) | Puntaje Final")
        .expect("Error al escribir encabezado");

    for res in resultados {
        // Formatear los puntajes individuales (ej: 7.80, 9.60, 6.80)
        let puntajes_str: String = res.puntajes_por_jurado.iter()
            .map(|p| format!("{:.2}", p))
            .collect::<Vec<String>>()
            .join(", ");
            
        // Formatear la línea final
        writeln!(&mut contenido, "{} | {} | {:.2}", 
                 res.nombre, 
                 puntajes_str, 
                 res.puntaje_final)
            .expect("Error al escribir línea de datos");
    }

    // Escribir todo el contenido al archivo
    fs::write(ruta, contenido.as_bytes())
}
use std::io;

fn main() {
    
    println!("--------Encuesta Para Las Redes Sociales-----------");

    // Primero leemos el número de personas a encuestar y lo convertimos la variable en número entero

    let mut numero_personas_tex= String::new();

    println!("Introduzca el número de personas que desea encuestar");    

    io::stdin()   //guardamos la variable
        .read_line(&mut numero_personas_tex);
        
    let numero_personas: i32 = numero_personas_tex 
        .trim()   // .trim() elimina el salto de línea (\n) al final del texto.
        .parse::<i32>()
        .expect("¡Eso no es un número entero válido!");

    // Declaramos las variables de las redes sociales que van hacer acumulativas

    let mut whatsapp: i32 = 0;
    let mut telegram: i32 = 0;
    let mut instagram: i32 = 0;
    let mut ninguna: i32 = 0;

    // Declaramos las variables de la primera persona que usa telegram
    let mut telegram_primera_persona:String = String::new();
    let mut telegram_persona_edad:String =String::new();
    let mut encontrado:bool = false ;

    //total de personas por genero
    let mut usuarios_femeninos: i32 = 0;
    let mut usuarios_masculinos: i32 = 0;

    //  realizamos la estructura repetitiva para X personas encuestadas
    // 0..num_personas define un rango semi-abierto.
    for i in 0.. numero_personas {

        println!("Encuesta para la Persona {}/{} ", i + 1, numero_personas);

        let mut nombre: String=String::new();
        let mut genero: String=String::new();
        let mut edad_tex: String =String::new() ;

        println!("Ingrese su Nombre: ");
        io::stdin()
            .read_line(&mut nombre);

        println!("Ingrese su Genero F/M: ");
        io::stdin()
            .read_line(&mut genero);

        println!("Ingrese su Edad: ");
        io::stdin()
            .read_line(&mut edad_tex);

        // Después de pedir los datos personales le pregunto por la red social más utilizada

        let mut red_social_utilizada_tex: String =String::new();
        
        println!("¿Cuál es la red social principal que utiliza?");
        println!("1 = WhatsApp");
        println!("2 = Telegram");
        println!("3 = Instagram");
        println!("4 = Ninguna");

        io::stdin()
            .read_line(&mut red_social_utilizada_tex);

        let mut red_social_utilizada:i32=red_social_utilizada_tex
            .trim()
            .parse::<i32>()
            .expect("¡Eso no es un número entero válido!");
       
        // Se usa el operador match es una versión superpoderosa del switch
        // Compara un valor con una serie de patrones y ejecuta el código asociado al primer patrón que coincide.
        match red_social_utilizada {
            1 => whatsapp += 1,
            2 => {
                    telegram += 1;
                    if encontrado == false {
                        telegram_primera_persona = nombre.trim().to_string();
                        telegram_persona_edad = edad_tex.trim().to_string();
                        encontrado=true;
                    }
                },
            3 => instagram += 1,
            4 => ninguna += 1,
            _ => println!("Opción fuera de rango (1-4). No se cuenta."),
        }
        // verificamos que genero utiliza mas las redes sociales
        // 1. Limpieza de Género: Convierte la entrada a un único char en mayúscula ('F' o 'M').
        let genero_char: char = genero // Inicia la limpieza de la cadena 'genero'
        .trim()                    
        .chars()            // Convierte la subcadena en un iterador de caracteres.
        .next()          // Obtiene el primer carácter introducido.
        .unwrap_or('?') // Usa '?' si el usuario no escribió nada.
        .to_uppercase()  // Convierte el carácter a mayúscula.
        .next()         // Toma el carácter resultante (p. ej., 'F' o 'M').
        .unwrap_or('?');    // Asegura que siempre se obtenga un carácter final.
            
        let genero_usa_red_social: bool= red_social_utilizada>=1 && red_social_utilizada<=3 ;

        if genero_usa_red_social && genero_char == 'F' {

            usuarios_femeninos +=1;

        } else if genero_usa_red_social && genero_char == 'M' {

             usuarios_masculinos += 1;
        }
    }
    // calculamos cual de las 3 redes es mas rentable invertir en publicidad.

    let red_mas_rentable:&str; 
    // Comparamos los contadores para encontrar el máximo
    if whatsapp > telegram && whatsapp > instagram {
        red_mas_rentable = "WhatsApp";
    } else if telegram > whatsapp && telegram > instagram {
        red_mas_rentable = "Telegram";
    } else if instagram > whatsapp && instagram > telegram {
        red_mas_rentable = "Instagram";
    } else {
    red_mas_rentable = "Hay un empate entre dos o más redes, o todas tienen cero usuarios";
    }

    // luego calculamos el total de todos los usuarios de las redes sociales

    let mut total_usuario_redes:i32  = whatsapp + telegram + instagram;

    // calculamos el porcentajes de numero de personas que usan las redes

    let total_usuarios_float: f64 = total_usuario_redes as f64;
    let numero_personas_float: f64 = numero_personas as f64;

    let mut porcentaje_usuario: f64 = (total_usuarios_float / numero_personas_float) * 100.0;
    
    // --------------------------------------------------------------------------

    println!("\n\n========================================================");
    println!("|               ANÁLISIS FINAL DE LA ENCUESTA            |");
    println!("========================================================");
    println!("Total de personas encuestadas: {}", numero_personas_tex);
    println!("--------------------------------------------------------");

    // 1. Cantidad de personas encuestadas que utilizan cada red
    println!("1. Uso de Redes Sociales (Conteo Absoluto):");
    println!("   - WhatsApp:  {} personas", whatsapp);
    println!("   - Telegram:  {} personas", telegram);
    println!("   - Instagram: {} personas", instagram);
    println!("   - Ninguna:   {} personas", ninguna);
    println!();

    // 2. Porcentaje de personas encuestadas que utilizan alguna de las tres principales redes
    println!("2. Porcentaje de Uso General:");
    println!("   -> Total de personas que usan alguna de las 3 redes: {}", total_usuario_redes);
    // Se usa {:.2} para mostrar el porcentaje con dos decimales.
    println!("   -> PORCENTAJE TOTAL DE USO: {:.2}%", porcentaje_usuario); 
    println!();

    // 3. Nombre y edad de la primera persona encuestada que usa TELEGRAM.
    println!("3. Primera Persona Registrada con TELEGRAM:");
    if encontrado {
        println!("   -> Nombre: {}", telegram_primera_persona);
        println!("   -> Edad:   {}", telegram_persona_edad); 
    } else {
        println!("   -> No se encontró a ninguna persona que use Telegram en la muestra.");
    }
    println!();

    // 4. ¿Cuál género utiliza más las redes sociales?
    println!("4. Uso de Redes por Género (WhatsApp/Telegram/Instagram):");
    println!("   - Total Femenino (F): {} usuarios", usuarios_femeninos);
    println!("   - Total Masculino (M): {} usuarios", usuarios_masculinos);
    println!();

    // 5. ¿En cuál de las tres redes sociales sería más rentable invertir en publicidad?
    println!("5. Conclusión de Rentabilidad (Mayor Audiencia):");
    println!("   -> La red más popular y rentable para invertir es: {}", red_mas_rentable);
    println!("--------------------------------------------------------");
    println!("¡Análisis completado!");
    println!("========================================================");
    
}

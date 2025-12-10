    /*Bibliotecas*/
    use std::io;

fn main() {
    /*Calculadora Básica*/

    println!("-------------Calculadora Básica--------------", );

    let mut numero1_texto = String::new();

    println!("Ingrese el Primer Numero: ");

    io::stdin()
        .read_line(&mut numero1_texto)
        .expect("Fallo al leer el numero");

    let numero1: f64 =numero1_texto
        .trim()
        .parse::<f64>()
        .expect("¡Por favor, ingresa un número válido para el primer valor!");

    println!("Ingresa la operación (+, -, *, /):");

    let mut operador_texto = String::new();

    io::stdin()
        .read_line(&mut operador_texto)
        .expect("Fallo al leer linea");

        // CONVERSIÓN DE OPERACIÓN:
        // .trim() elimina espacios, .chars() obtiene un iterador de caracteres, y .next() toma el primero.
        // .unwrap() toma ese primer carácter.
    let operador: char = operador_texto
        .trim()
        .chars()
        .next()
        .unwrap(); 

    let mut numero2_texto = String::new();

    println!("Ingrese el Segundo Numero: ");

    io::stdin()
        .read_line(&mut numero2_texto)
        .expect("Fallo al leer el numero");

    let numero2 : f64 = numero2_texto
        .trim()
        .parse::<f64>()
        .expect("¡Por favor, ingresa un número válido para el segundo valor!");

    let mut resultado = 0.0;

    match operador {
            // Caso de Suma
        '+' => {
            resultado = numero1 + numero2;
        },
        // Caso de Resta
        '-' => {
            resultado = numero1 - numero2;
        },
        // Caso de Multiplicación
        '*' => {
            resultado = numero1 * numero2;
        },
        // Caso de Divicion
        '/'=> {
                if numero2 != 0.0 {
                    resultado = numero1 / numero2;
                }else {
                    println!("Error: ¡División por cero no permitida!");
                    return;
                }                
        },
         // Wildcard: Cualquier otro carácter
         _ => {
            println!("Error: Operación no reconocida. Usa +, -, *, /.");
            return; // Termina la función main
        }
    }
    println!("El resultado de {} {} {} es {}",numero1,operador,numero2,resultado);

}
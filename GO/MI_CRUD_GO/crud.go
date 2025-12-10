package main

import (
	"database/sql" // Paquete estándar para interactuar con bases de datos SQL.
	"fmt"          // Paquete para formatear e imprimir cadenas.
	"log"          // Paquete para registrar mensajes (errores fatales, etc.).

	_ "github.com/lib/pq" // Importa el driver de PostgreSQL. El '_' indica que no lo usaremos directamente,
	// pero necesitamos que se inicialice para registrarse con el paquete database/sql.
)

// --- Configuración de la Base de Datos ---
// Definimos las constantes para los parámetros de conexión.
// ¡Asegúrate de que estos valores coincidan con tu configuración de PostgreSQL!
const (
	dbHost     = "localhost"
	dbPort     = 5432
	dbUser     = "postgres"
	dbPassword = "123" // <-- ¡IMPORTANTE! Reemplaza esto con tu contraseña real de PostgreSQL.
	dbName     = "clientes"
)

// Estructura para representar un dato personal.
// Usamos campos exportados (inician con mayúscula) para que puedan ser accedidos fuera del paquete.
type DatoPersonal struct {
	CI       string
	Nombre   string
	Apellido string
}

// --- Función para Conectar a la Base de Datos ---
// ConnectDB abre y devuelve una conexión a la base de datos PostgreSQL.
// Retorna un puntero a sql.DB que representa el pool de conexiones.
func ConnectDB() *sql.DB {
	// Construye la cadena de conexión DSN (Data Source Name).
	// sslmode=disable es común para desarrollo local.
	connStr := fmt.Sprintf("host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
		dbHost, dbPort, dbUser, dbPassword, dbName)

	// sql.Open no establece la conexión inmediatamente, solo valida los parámetros.
	// Retorna un objeto *sql.DB que representa un pool de conexiones.
	db, err := sql.Open("postgres", connStr)
	if err != nil {
		// log.Fatalf detiene la ejecución del programa si hay un error fatal.
		log.Fatalf("Error abriendo la conexión a la base de datos: %v", err)
	}

	// db.Ping() intenta establecer una conexión real para verificar que los datos de conexión son válidos.
	err = db.Ping()
	if err != nil {
		log.Fatalf("Error conectando a la base de datos (ping falló): %v", err)
	}

	fmt.Println("Conexión a la base de datos PostgreSQL exitosa!")
	return db
}

// --- Función para Crear un Nuevo Registro ---
// CreateDato inserta un nuevo registro en la tabla datos_personales.
// Recibe el objeto *sql.DB (el pool de conexiones) y los datos a insertar.
func CreateDato(db *sql.DB, ci, nombre, apellido string) {
	// Consulta SQL para insertar datos, usando marcadores de posición posicionales ($1, $2, $3).
	// Estos son seguros contra inyecciones SQL.
	sqlStatement := `INSERT INTO public.datos_personales (ci, nombre, apellido) VALUES ($1, $2, $3)`

	// db.Exec ejecuta una consulta que no devuelve filas (INSERT, UPDATE, DELETE).
	// El segundo argumento son los valores para los marcadores de posición.
	_, err := db.Exec(sqlStatement, ci, nombre, apellido)
	if err != nil {
		// Imprime el error pero permite que el programa continúe.
		fmt.Printf("Error al crear registro: %v\n", err)
		return // Sale de la función
	}
	fmt.Printf("Registro creado exitosamente: CI=%s, Nombre=%s, Apellido=%s\n", ci, nombre, apellido)
}

// --- Función para Leer (Obtener) Registros ---
// ReadDatos lee y muestra todos los registros de la tabla datos_personales.
func ReadDatos(db *sql.DB) {
	// Consulta SQL para seleccionar todos los datos.
	sqlStatement := `SELECT ci, nombre, apellido FROM public.datos_personales`

	// db.Query ejecuta una consulta que devuelve un conjunto de filas (SELECT).
	rows, err := db.Query(sqlStatement)
	if err != nil {
		fmt.Printf("Error al leer registros: %v\n", err)
		return
	}
	// 'defer rows.Close()' asegura que las filas se cierren cuando la función retorne,
	// liberando recursos de la base de datos. Esto es crucial.
	defer rows.Close()

	fmt.Println("\n--- Registros en la Base de Datos ---")
	found := false // Bandera para saber si se encontraron registros
	// rows.Next() avanza al siguiente registro y devuelve true si hay más.
	for rows.Next() {
		found = true
		var dato DatoPersonal // Crea una nueva instancia de DatoPersonal para cada fila.
		// rows.Scan asigna los valores de las columnas de la fila actual a las variables.
		err = rows.Scan(&dato.CI, &dato.Nombre, &dato.Apellido)
		if err != nil {
			fmt.Printf("Error al escanear registro: %v\n", err)
			continue // Continúa con la siguiente fila si hay un error en esta.
		}
		fmt.Printf("CI: %s, Nombre: %s, Apellido: %s\n", dato.CI, dato.Nombre, dato.Apellido)
	}
	if !found {
		fmt.Println("No hay registros en la tabla datos_personales.")
	}
	fmt.Println("------------------------------------")

	// rows.Err() verifica si ocurrió algún error durante la iteración de las filas.
	err = rows.Err()
	if err != nil {
		fmt.Printf("Error durante la iteración de registros: %v\n", err)
	}
}

// --- Función para Actualizar un Registro ---
// UpdateDato actualiza el nombre y apellido de un registro existente por su CI.
func UpdateDato(db *sql.DB, ci, nuevoNombre, nuevoApellido string) {
	// Consulta SQL para actualizar datos con marcadores de posición.
	sqlStatement := `UPDATE public.datos_personales SET nombre = $1, apellido = $2 WHERE ci = $3`

	// Ejecuta la consulta de actualización.
	result, err := db.Exec(sqlStatement, nuevoNombre, nuevoApellido, ci)
	if err != nil {
		fmt.Printf("Error al actualizar registro: %v\n", err)
		return
	}

	// result.RowsAffected() devuelve el número de filas que fueron afectadas por la operación.
	rowsAffected, err := result.RowsAffected()
	if err != nil {
		fmt.Printf("Error al obtener filas afectadas: %v\n", err)
		return
	}

	if rowsAffected > 0 {
		fmt.Printf("Registro con CI %s actualizado exitosamente.\n", ci)
	} else {
		fmt.Printf("No se encontró ningún registro con CI %s para actualizar.\n", ci)
	}
}

// --- Función para Borrar un Registro ---
// DeleteDato borra un registro de la tabla datos_personales por su CI.
func DeleteDato(db *sql.DB, ci string) {
	// Consulta SQL para borrar datos.
	sqlStatement := `DELETE FROM public.datos_personales WHERE ci = $1`

	// Ejecuta la consulta de borrado.
	result, err := db.Exec(sqlStatement, ci)
	if err != nil {
		fmt.Printf("Error al borrar registro: %v\n", err)
		return
	}

	// Verifica cuántas filas fueron afectadas.
	rowsAffected, err := result.RowsAffected()
	if err != nil {
		fmt.Printf("Error al obtener filas afectadas: %v\n", err)
		return
	}

	if rowsAffected > 0 {
		fmt.Printf("Registro con CI %s borrado exitosamente.\n", ci)
	} else {
		fmt.Printf("No se encontró ningún registro con CI %s para borrar.\n", ci)
	}
}

// --- Bloque Principal de Ejecución (Función main) ---
// La función 'main' es el punto de entrada de cualquier programa Go ejecutable.
func main() {
	fmt.Println("\n--- Demostración de Operaciones CRUD en Go ---")

	// 1. Conectar a la base de datos.
	db := ConnectDB()

	// liberando todos los recursos de la base de datos.
	defer db.Close()

	// Datos de ejemplo que usaremos para las operaciones CRUD.
	ciEjemplo := "1234567890"
	nombreEjemplo := "Juan"
	apellidoEjemplo := "Pérez"

	// --- DEMOSTRACIÓN DE OPERACIONES ---

	// 2. Crear un registro.
	fmt.Println("\n--- 1. Creando un nuevo registro ---")
	CreateDato(db, ciEjemplo, nombreEjemplo, apellidoEjemplo)

	// 3. Leer registros.
	fmt.Println("\n--- 2. Leyendo todos los registros ---")
	ReadDatos(db)

	// 4. Actualizar un registro.
	fmt.Println("\n--- 3. Actualizando el registro ---")

	// Cambiamos el nombre y apellido del registro creado.
	UpdateDato(db, ciEjemplo, "Juanito", "Pérez García")

	// 5. Leer registros nuevamente para ver el cambio.
	fmt.Println("\n--- 4. Leyendo registros después de actualizar ---")
	ReadDatos(db)

	// 6. Borrar un registro.
	fmt.Println("\n--- 5. Borrando el registro ---")
	DeleteDato(db, ciEjemplo)

	// 7. Leer registros por última vez para confirmar que el registro fue borrado.
	fmt.Println("\n--- 6. Leyendo registros después de borrar ---")
	ReadDatos(db) // Esto debería mostrar "No hay registros..." si todo fue bien.

	fmt.Println("\n--- Demostración CRUD en Go Finalizada ---")

}

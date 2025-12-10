package main

import (
	"database/sql"
	"log"
	"net/http"
	"strconv"
	"text/template" // Usamos text/template, pero para producción se recomienda html/template por seguridad.

	_ "github.com/go-sql-driver/mysql" // Driver de MySQL
)

// Empleado es la estructura para mapear los datos de la tabla 'empleados'
type Empleado struct {
	Id     int
	Nombre string
	Correo string
}

// plantillas carga todos los archivos .tmpl de la carpeta 'plantillas'
var plantillas = template.Must(template.ParseGlob("plantillas/*"))

// db es la conexión global a la base de datos
var db *sql.DB

func main() {
	var err error
	// Conexión a la base de datos MySQL. Ajusta las credenciales si es necesario.
	// Formato: "usuario:contraseña@tcp(host:puerto)/nombre_bd"
	db, err = sql.Open("mysql", "root:@tcp(127.0.0.1:3306)/sistema")
	if err != nil {
		log.Fatalf("Error al conectar a la base de datos: %v", err)
	}
	defer db.Close() // Asegura que la conexión se cierre al finalizar main

	// Verifica la conexión a la base de datos
	err = db.Ping()
	if err != nil {
		log.Fatalf("Error al hacer ping a la base de datos: %v", err)
	}
	log.Println("Conexión a la base de datos MySQL establecida correctamente!")

	// Manejadores de rutas HTTP
	http.HandleFunc("/", Inicio)
	http.HandleFunc("/crear", Crear)
	http.HandleFunc("/insertar", Insertar)
	http.HandleFunc("/borrar", Borrar)
	http.HandleFunc("/editar", Editar)
	http.HandleFunc("/actualizar", Actualizar)

	log.Println("Servidor corriendo en http://localhost:8080")
	log.Fatal(http.ListenAndServe(":8080", nil)) // Inicia el servidor
}

// Inicio: Muestra la lista de empleados
func Inicio(w http.ResponseWriter, r *http.Request) {
	filas, err := db.Query("SELECT id, nombre, correo FROM empleados ORDER BY id DESC")
	if err != nil {
		log.Printf("Error al consultar empleados: %v", err)
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}
	defer filas.Close()

	empleados := []Empleado{}
	for filas.Next() {
		var empleado Empleado
		if err := filas.Scan(&empleado.Id, &empleado.Nombre, &empleado.Correo); err != nil {
			log.Printf("Error al escanear empleado: %v", err)
			http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
			return
		}
		empleados = append(empleados, empleado)
	}

	// Ejecuta la plantilla "inicio" y le pasa la lista de empleados
	plantillas.ExecuteTemplate(w, "inicio", empleados)
}

// Crear: Muestra el formulario para añadir un nuevo empleado
func Crear(w http.ResponseWriter, r *http.Request) {
	plantillas.ExecuteTemplate(w, "crear", nil)
}

// Insertar: Procesa el formulario de creación y guarda el nuevo empleado
func Insertar(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		nombre := r.FormValue("nombre")
		correo := r.FormValue("correo")

		if nombre == "" || correo == "" {
			http.Error(w, "Nombre y correo son campos obligatorios.", http.StatusBadRequest)
			return
		}

		insertarReg, err := db.Prepare("INSERT INTO empleados(nombre, correo) VALUES(?,?)")
		if err != nil {
			log.Printf("Error al preparar la inserción: %v", err)
			http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
			return
		}
		defer insertarReg.Close()

		_, err = insertarReg.Exec(nombre, correo)
		if err != nil {
			log.Printf("Error al ejecutar la inserción: %v", err)
			http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
			return
		}

		http.Redirect(w, r, "/", http.StatusFound) // Redirige a la página principal
	}
}

// Borrar: Elimina un empleado por su ID
func Borrar(w http.ResponseWriter, r *http.Request) {
	idEmpleadoStr := r.URL.Query().Get("id")
	if idEmpleadoStr == "" {
		http.Error(w, "ID de empleado no proporcionado.", http.StatusBadRequest)
		return
	}

	borrarReg, err := db.Prepare("DELETE FROM empleados WHERE id=?")
	if err != nil {
		log.Printf("Error al preparar el borrado: %v", err)
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}
	defer borrarReg.Close()

	_, err = borrarReg.Exec(idEmpleadoStr)
	if err != nil {
		log.Printf("Error al ejecutar el borrado: %v", err)
		http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		return
	}

	http.Redirect(w, r, "/", http.StatusFound)
}

// Editar: Muestra el formulario de edición con los datos del empleado
func Editar(w http.ResponseWriter, r *http.Request) {
	idEmpleadoStr := r.URL.Query().Get("id")
	if idEmpleadoStr == "" {
		http.Error(w, "ID de empleado no proporcionado.", http.StatusBadRequest)
		return
	}

	fila := db.QueryRow("SELECT id, nombre, correo FROM empleados WHERE id=?", idEmpleadoStr)

	var empleado Empleado
	if err := fila.Scan(&empleado.Id, &empleado.Nombre, &empleado.Correo); err != nil {
		if err == sql.ErrNoRows {
			http.Error(w, "Empleado no encontrado.", http.StatusNotFound)
		} else {
			log.Printf("Error al escanear empleado para edición: %v", err)
			http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
		}
		return
	}

	plantillas.ExecuteTemplate(w, "editar", empleado)
}

// Actualizar: Procesa el formulario de edición y actualiza los datos del empleado
func Actualizar(w http.ResponseWriter, r *http.Request) {
	if r.Method == "POST" {
		idStr := r.FormValue("id")
		nombre := r.FormValue("nombre")
		correo := r.FormValue("correo")

		if idStr == "" || nombre == "" || correo == "" {
			http.Error(w, "Todos los campos son obligatorios.", http.StatusBadRequest)
			return
		}

		// Convertir el ID de string a int
		id, err := strconv.Atoi(idStr)
		if err != nil {
			http.Error(w, "ID de empleado inválido.", http.StatusBadRequest)
			return
		}

		actualizarReg, err := db.Prepare("UPDATE empleados SET nombre=?, correo=? WHERE id=?")
		if err != nil {
			log.Printf("Error al preparar la actualización: %v", err)
			http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
			return
		}
		defer actualizarReg.Close()

		_, err = actualizarReg.Exec(nombre, correo, id)
		if err != nil {
			log.Printf("Error al ejecutar la actualización: %v", err)
			http.Error(w, "Error interno del servidor", http.StatusInternalServerError)
			return
		}

		http.Redirect(w, r, "/", http.StatusFound)
	}
}

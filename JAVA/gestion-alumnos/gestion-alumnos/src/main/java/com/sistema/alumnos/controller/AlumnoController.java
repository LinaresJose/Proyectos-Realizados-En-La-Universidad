package com.sistema.alumnos.controller;

import com.sistema.alumnos.model.Alumno;
import com.sistema.alumnos.service.AlumnoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

// 1. ANOTACIONES PRINCIPALES
@RestController // Combina @Controller y @ResponseBody (para devolver JSON)
@RequestMapping("/api/alumnos") // Define la URL base para todos los métodos
public class AlumnoController {

    // 2. INYECCIÓN DEL SERVICIO
    @Autowired
    private AlumnoService alumnoService;

    // ----------------------------------------------------------------------
    // 3. C (CREATE) - CREAR UN NUEVO ALUMNO
    // Petición: POST /api/alumnos
    // ----------------------------------------------------------------------
    @PostMapping
    public ResponseEntity<Alumno> crearAlumno(@RequestBody Alumno alumno) {
        // El @RequestBody convierte el JSON entrante a un objeto Alumno
        Alumno nuevoAlumno = alumnoService.guardarOActualizarAlumno(alumno);
        // Devolvemos el alumno creado con el estado 201 CREATED
        return new ResponseEntity<>(nuevoAlumno, HttpStatus.CREATED);
    }

    // ----------------------------------------------------------------------
    // 4. R (READ) - LEER TODOS
    // Petición: GET /api/alumnos
    // ----------------------------------------------------------------------
    @GetMapping
    public List<Alumno> obtenerTodos() {
        return alumnoService.obtenerTodos();
    }

    // 5. R (READ) - LEER POR ID
    // Petición: GET /api/alumnos/{id}
    // ----------------------------------------------------------------------
    @GetMapping("/{id}")
    public ResponseEntity<Alumno> obtenerPorId(@PathVariable Long id) {

        // Usamos el Optional devuelto por el Service
        return alumnoService.obtenerPorId(id)
                // .map(ResponseEntity::ok) -> Si Optional tiene valor (Alumno), devuelve 200 OK con el cuerpo
                .map(ResponseEntity::ok)
                // .orElseGet -> Si Optional está vacío, devuelve 404 Not Found
                .orElseGet(() -> ResponseEntity.notFound().build());
    }

    // ----------------------------------------------------------------------
    // 6. U (UPDATE) - ACTUALIZAR
    // Petición: PUT /api/alumnos/{id}
    // ----------------------------------------------------------------------
    @PutMapping("/{id}")
    public ResponseEntity<Alumno> actualizarAlumno(@PathVariable Long id, @RequestBody Alumno alumnoDetalles) {

        // 1. Intentamos encontrar el alumno por ID
        return alumnoService.obtenerPorId(id)
                .map(alumnoExistente -> {
                    // 2. Si existe: Actualizamos los campos con los nuevos detalles
                    alumnoExistente.setNombre(alumnoDetalles.getNombre());
                    alumnoExistente.setApellido(alumnoDetalles.getApellido());
                    alumnoExistente.setCedula(alumnoDetalles.getCedula());
                    alumnoExistente.setDireccion(alumnoDetalles.getDireccion());
                    alumnoExistente.setEdad(alumnoDetalles.getEdad());
                    alumnoExistente.setCarrera(alumnoDetalles.getCarrera());

                    // 3. Guardamos los cambios (UPDATE)
                    Alumno actualizado = alumnoService.guardarOActualizarAlumno(alumnoExistente);
                    return new ResponseEntity<>(actualizado, HttpStatus.OK); // Retorna 200
                })
                .orElseGet(() -> ResponseEntity.notFound().build()); // 4. Si no existe: Retorna 404
    }

    // ----------------------------------------------------------------------
    // 7. D (DELETE) - ELIMINAR
    // Petición: DELETE /api/alumnos/{id}
    // ----------------------------------------------------------------------
    @DeleteMapping("/{id}")
    public ResponseEntity<Void> eliminarAlumno(@PathVariable Long id) {
        alumnoService.eliminarAlumno(id);
        // Devolvemos el estado 204 NO_CONTENT (éxito sin cuerpo de respuesta)
        return new ResponseEntity<>(HttpStatus.NO_CONTENT);
    }
}
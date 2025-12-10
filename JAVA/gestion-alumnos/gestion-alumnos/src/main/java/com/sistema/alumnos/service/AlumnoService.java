package com.sistema.alumnos.service;

import com.sistema.alumnos.model.Alumno;
import com.sistema.alumnos.repository.AlumnoRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

// Anotación que marca esta clase como un componente de servicio de Spring
@Service
public class AlumnoService {

    // Inyección de Dependencia: Spring crea una instancia de AlumnoRepository para nosotros
    @Autowired
    private AlumnoRepository alumnoRepository;

    // --- C (Crear) y U (Actualizar) ---
    // Simplemente delega la llamada al repositorio
    public Alumno guardarOActualizarAlumno(Alumno alumno) {
        // En un caso real, la lógica de validación o transformación iría antes de llamar a save.
        return alumnoRepository.save(alumno);
    }

    // --- R (Leer Todos) ---
    public List<Alumno> obtenerTodos() {
        return alumnoRepository.findAll();
    }

    // --- R (Leer por ID) ---
    // Devuelve un Optional<Alumno> porque el alumno podría no existir
    public Optional<Alumno> obtenerPorId(Long id) {
        return alumnoRepository.findById(id);
    }

    // --- D (Eliminar) ---
    public void eliminarAlumno(Long id) {
        alumnoRepository.deleteById(id);
    }
}
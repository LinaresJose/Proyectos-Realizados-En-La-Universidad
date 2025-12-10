package com.sistema.alumnos.repository;

import com.sistema.alumnos.model.Alumno;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

// La anotación @Repository marca esta interfaz como un componente de acceso a datos de Spring.
@Repository
public interface AlumnoRepository extends JpaRepository<Alumno, Long> {

    // NOTA: No necesitamos escribir ningún método aquí.
    // Todos los métodos CRUD (save, findById, findAll, deleteById)
    // se heredan automáticamente de JpaRepository.
}
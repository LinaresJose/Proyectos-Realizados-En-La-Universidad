package com.sistema.alumnos.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
import jakarta.persistence.Table;

// 1. ANOTACIÓN DE ENTIDAD JPA
@Entity
// Opcional: Especifica el nombre de la tabla en la base de datos.
@Table(name = "alumnos")
public class Alumno {

    // 2. CLAVE PRIMARIA (ID)
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id; // Usamos Long para IDs autoincrementales

    // 3. CAMPOS DE LA TABLA

    // El nombre no puede ser nulo en la base de datos
    @Column(nullable = false)
    private String nombre;

    private String apellido;

    // La cédula debe ser única y no nula (es un identificador clave)
    @Column(unique = true, nullable = false)
    private String cedula;

    private String direccion;
    private Integer edad;
    private String carrera;

    // 4. CONSTRUCTOR VACÍO (Requisito MANDATORIO de JPA/Hibernate)
    public Alumno() {
    }

    // 5. GETTERS Y SETTERS (Permiten a Spring leer y escribir los valores)

    // --- Getters ---
    public Long getId() {
        return id;
    }

    public String getNombre() {
        return nombre;
    }

    public String getApellido() {
        return apellido;
    }

    public String getCedula() {
        return cedula;
    }

    public String getDireccion() {
        return direccion;
    }

    public Integer getEdad() {
        return edad;
    }

    public String getCarrera() {
        return carrera;
    }

    // --- Setters ---
    public void setId(Long id) {
        this.id = id;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public void setApellido(String apellido) {
        this.apellido = apellido;
    }

    public void setCedula(String cedula) {
        this.cedula = cedula;
    }

    public void setDireccion(String direccion) {
        this.direccion = direccion;
    }

    public void setEdad(Integer edad) {
        this.edad = edad;
    }

    public void setCarrera(String carrera) {
        this.carrera = carrera;
    }
}
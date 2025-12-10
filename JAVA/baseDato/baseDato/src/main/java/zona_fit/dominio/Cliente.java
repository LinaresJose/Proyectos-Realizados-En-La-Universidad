package zona_fit.dominio;

import java.util.Objects;

public class Cliente {
    private int id;
    private String nombre;
    private String apellido;
    private int membresia;
    private int edad;

    public Cliente(){}

    public Cliente(int id){
        this.id = id;
    }

    public Cliente(String nombre, String apellido, int membresia, int edad){
        this.nombre = nombre;
        this.apellido = apellido;
        this.membresia = membresia;
        this.edad=edad;
    }

    public Cliente(int id, String nombre, String apellido, int membresia, int edad){
        this(nombre, apellido, membresia, edad);
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public String getApellido() {
        return apellido;
    }

    public void setApellido(String apellido) {
        this.apellido = apellido;
    }

    public int getMembresia() {
        return membresia;
    }

    public void setMembresia(int membresia) {
        this.membresia = membresia;
    }

    public int getEdad() {
        return edad;
    }

    public void setEdad(int edad) {
        this.edad = edad;
    }

    @Override
    public String toString() {
        return "Cliente{" +
                "id=" + id +
                ", nombre='" + nombre + '\'' +
                ", apellido='" + apellido + '\'' +
                ", membresia=" + membresia + '\'' +
                ", edad=" + edad +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Cliente cliente = (Cliente) o;
        return id == cliente.id && membresia == cliente.membresia && Objects.equals(nombre, cliente.nombre) && Objects.equals(apellido, cliente.apellido);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, nombre, apellido, membresia);
    }
   /*
    public static void main(String[] args) {
        Cliente cliente = new Cliente(1,"Pedro", "Ortiz",2);
        System.out.println( cliente.getNombre());
    }
    */

}

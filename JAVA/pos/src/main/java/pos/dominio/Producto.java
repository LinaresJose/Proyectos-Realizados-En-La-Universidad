package pos.dominio;

import java.util.Objects;
import java.text.NumberFormat;
import java.util.Locale;

public class Producto {

    private int id;
    private String nombre;
    private int cantidad;
    private double precio;
    private String descripcion;

    // 1. Constructor vacío (para listar)
    public Producto() {}

    // 2. Constructor por ID (para buscar o eliminar)
    public Producto(int id) {
        this.id = id;
    }

    // 3. Constructor para agregar (sin ID)
    public Producto(String nombre, int cantidad, double precio, String descripcion) {
        this.nombre = nombre;
        this.cantidad = cantidad;
        this.precio = precio;
        this.descripcion = descripcion;
    }

    // 4. Constructor para modificar (con ID)
    public Producto(int id, String nombre, int cantidad, double precio, String descripcion) {
        this(nombre, cantidad, precio, descripcion);
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getCantidad() {
        return cantidad;
    }

    public void setCantidad(int cantidad) {
        this.cantidad = cantidad;
    }

    public String getNombre() {
        return nombre;
    }

    public void setNombre(String nombre) {
        this.nombre = nombre;
    }

    public double getPrecio() {
        return precio;
    }

    public void setPrecio(double precio) {
        this.precio = precio;
    }

    public String getDescripcion() {
        return descripcion;
    }

    public void setDescripcion(String descripcion) {
        this.descripcion = descripcion;
    }

    @Override
    public String toString() {
        // Obtenemos el formateador de moneda para($)
        NumberFormat currencyFormatter = NumberFormat.getCurrencyInstance(Locale.US);
        // Formateamos el precio
        String precioFormateado = currencyFormatter.format(this.precio);

        return "Producto{" +
                "id = " + id +
                ", nombre = '" + nombre + '\'' +
                ", cantidad = " + cantidad +
                ", precio = " + precioFormateado +
                ", descripcion = '" + descripcion + '\'' +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (o == null || getClass() != o.getClass()) return false;
        Producto producto = (Producto) o;
        return id == producto.id && cantidad == producto.cantidad && Double.compare(precio, producto.precio) == 0 && Objects.equals(nombre, producto.nombre) && Objects.equals(descripcion, producto.descripcion);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, nombre, cantidad, precio, descripcion);
    }
}

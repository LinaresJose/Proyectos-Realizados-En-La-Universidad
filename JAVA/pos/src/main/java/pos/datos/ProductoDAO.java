package pos.datos;

import pos.dominio.Producto;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

// Asume que tienes un paquete de conexión, por ejemplo:
import static pos.conexion.Conexion.getConexion; // <-- ¡ADAPTA ESTE IMPORT!

public class ProductoDAO implements IProductoDAO {

    // QUERY DE LECTURA (READ)
    @Override
    public List<Producto> listarProductos() {
        List<Producto> productos = new ArrayList<>();
        Connection con = getConexion();
        var sql = "SELECT * FROM producto ORDER BY id";
        try (PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {

            while (rs.next()) {
                var producto = new Producto();
                producto.setId(rs.getInt("id"));
                producto.setNombre(rs.getString("nombre"));
                producto.setCantidad(rs.getInt("cantidad"));
                producto.setPrecio(rs.getDouble("precio"));
                producto.setDescripcion(rs.getString("descripcion"));
                productos.add(producto);
            }
        } catch (Exception e) {
            System.out.println("Error al listar productos: " + e.getMessage());
        } finally {
            try {
                if (con != null) con.close();
            } catch (Exception e) {
                System.out.println("Error al cerrar conexión: " + e.getMessage());
            }
        }
        return productos;
    }

    // QUERY DE BUSQUEDA
    @Override
    public boolean buscarProductoPorId(Producto producto) {
        Connection con = getConexion();
        var sql = "SELECT * FROM producto WHERE id = ?";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, producto.getId());
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    producto.setNombre(rs.getString("nombre"));
                    producto.setCantidad(rs.getInt("cantidad"));
                    producto.setPrecio(rs.getDouble("precio"));
                    producto.setDescripcion(rs.getString("descripcion"));
                    return true;
                }
            }
        } catch (Exception e) {
            System.out.println("Error al buscar producto: " + e.getMessage());
        } finally {
            try {
                if (con != null) con.close();
            } catch (Exception e) {
                System.out.println("Error al cerrar conexión: " + e.getMessage());
            }
        }
        return false;
    }

    // QUERY DE CREACION (CREATE)
    @Override
    public boolean agregarProducto(Producto producto) {
        Connection con = getConexion();
        var sql = "INSERT INTO producto(nombre, cantidad, precio, descripcion) VALUES(?, ?, ?, ?)";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setString(1, producto.getNombre());
            ps.setInt(2, producto.getCantidad());
            ps.setDouble(3, producto.getPrecio());
            ps.setString(4, producto.getDescripcion());
            return ps.executeUpdate() == 1;
        } catch (Exception e) {
            System.out.println("Error al agregar producto: " + e.getMessage());
        } finally {
            try {
                if (con != null) con.close();
            } catch (Exception e) {
                System.out.println("Error al cerrar conexión: " + e.getMessage());
            }
        }
        return false;
    }

    // QUERY DE ACTUALIZACION (UPDATE)
    @Override
    public boolean modificarProducto(Producto producto) {
        Connection con = getConexion();
        var sql = "UPDATE producto SET nombre=?, cantidad=?, precio=?, descripcion=? WHERE id = ?";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setString(1, producto.getNombre());
            ps.setInt(2, producto.getCantidad());
            ps.setDouble(3, producto.getPrecio());
            ps.setString(4, producto.getDescripcion());
            ps.setInt(5, producto.getId()); // El ID va al final
            return ps.executeUpdate() == 1;
        } catch (Exception e) {
            System.out.println("Error al modificar producto: " + e.getMessage());
        } finally {
            try {
                if (con != null) con.close();
            } catch (Exception e) {
                System.out.println("Error al cerrar conexión: " + e.getMessage());
            }
        }
        return false;
    }

    // QUERY DE ELIMINACION (DELETE)
    @Override
    public boolean eliminarProducto(Producto producto) {
        Connection con = getConexion();
        var sql = "DELETE FROM producto WHERE id = ?";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, producto.getId());
            return ps.executeUpdate() == 1;
        } catch (Exception e) {
            System.out.println("Error al eliminar producto: " + e.getMessage());
        } finally {
            try {
                if (con != null) con.close();
            } catch (Exception e) {
                System.out.println("Error al cerrar conexión: " + e.getMessage());
            }
        }
        return false;
    }

}

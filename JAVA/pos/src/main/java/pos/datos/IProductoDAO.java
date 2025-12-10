package pos.datos;

import pos.dominio.Producto;

import java.util.List;

public interface IProductoDAO {
    // QUERY DE LECTURA (READ)
    List<Producto> listarProductos();

    // QUERY DE BUSQUEDA
    boolean buscarProductoPorId(Producto producto);

    // QUERY DE CREACION (CREATE)
    boolean agregarProducto(Producto producto);

    // QUERY DE ACTUALIZACION (UPDATE)
    boolean modificarProducto(Producto producto);

    // QUERY DE ELIMINACION (DELETE)
    boolean eliminarProducto(Producto producto);
}

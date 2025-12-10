import javax.swing.*; // Importa todas las clases de Swing
import java.awt.FlowLayout; // Importa el gestor de diseño FlowLayout
import java.awt.event.ActionEvent; // Clase para manejar el evento de botón
import java.awt.event.ActionListener; // Interfaz para manejar el evento de botón

public class ElementosBasicosSwing extends JFrame implements ActionListener {

    // 1. Declaración de Componentes
    private JLabel etiqueta;
    private JTextField campoTexto;
    private JButton botonAceptar;

    public ElementosBasicosSwing() {
        // Configuración de la Ventana Principal (JFrame)
        setTitle("Formulario Básico con Swing"); // Título de la ventana
        setSize(400, 150); // Tamaño de la ventana: 400px de ancho, 150px de alto
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); // Finaliza la aplicación al cerrar la ventana
        setLayout(new FlowLayout()); // Usa FlowLayout: organiza los componentes de izquierda a derecha

        // 2. Inicialización de Componentes
        etiqueta = new JLabel("Ingrese su nombre:");
        campoTexto = new JTextField(20); // 20 columnas de ancho visible
        botonAceptar = new JButton("Aceptar");

        // 3. Registro del Listener (Gestión de Eventos)
        botonAceptar.addActionListener(this); // 'this' se refiere a esta clase, que implementa ActionListener

        // 4. Adición de Componentes al Contenedor (JFrame)
        add(etiqueta);
        add(campoTexto);
        add(botonAceptar);

        // Hace visible la ventana al final
        setVisible(true);
    }

    // 5. Método del Listener: Define la acción al presionar el botón
    @Override
    public void actionPerformed(ActionEvent e) {
        // Capturamos el texto del JTextField
        String nombre = campoTexto.getText();

        // Mostramos un mensaje emergente (JDialog)
        JOptionPane.showMessageDialog(this, "¡Bienvenido, " + nombre + "!");

        // Limpiamos el campo
        campoTexto.setText("");
    }

    // Método principal para ejecutar la aplicación
    public static void main(String[] args) {
        // Se recomienda ejecutar la GUI en el Event Dispatch Thread (EDT)
        SwingUtilities.invokeLater(() -> {
            new ElementosBasicosSwing(); // Crea e inicializa la ventana
        });
    }
}

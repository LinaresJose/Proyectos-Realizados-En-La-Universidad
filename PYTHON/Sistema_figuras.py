# --- Jose Linares. C.I: 27.952.174 ---
# --- clase padre ---
class Figura:
    def __init__(self,nombre):
        self._nombre=None
        self.nombre = nombre
    
    @property
    def nombre (self):
        
        return self._nombre
    
    @nombre.setter
    def nombre(self,validar_nombre):
        if not isinstance(validar_nombre,str) or not validar_nombre.strip():  # esto valida el nombre que sea string y espacio vacio
            
            raise ValueError("Ingrese un nombre valido para la figura Geométrica.")
    
        self._nombre=validar_nombre.strip().title() # se guarda el nombre sin espacios extra, y la primera letra en mayuscula
    
    def calcular_area(self):
        raise  NotImplementedError("Este metodo es para que las clases hijas calculen el area")
    
    def calcular_perimetro(self):
        raise NotImplementedError("Este metodo es para que las clases hijas calculen el perimetro")
        
    def mostrar_info(self):
        print("\n--- Información de la Figura ---\n")
        print(f"Nombre de la figura: {self.nombre}\n")
        
        area_calculada = self.calcular_area() 
        print(f"Su area es: {area_calculada:.2f} m²\n")
        
        perimetro_calculado = self.calcular_perimetro()
        print(f"Su perimetro es: {perimetro_calculado:.2f} m\n")
    
# --- clase hija Circulo --- 
import math # importar funciones y constantes para calcular el area y perimetro de un circulo (PI) π

class Circulo(Figura):
    def __init__(self,radio, nombre):
        super().__init__(nombre)
    
        self._radio=None
        self.radio=radio
    
    @property
    def radio(self):
        return self._radio
    
    @radio.setter
    def radio(self,validar_radio):
        if not isinstance(validar_radio,(int,float)): # esto es para validar que no sea un string
            raise TypeError("Ingre un numero valido para el radio.")
        if validar_radio <= 0:                        # Y esto para que sea un numero positivo
            raise TypeError("El radio debe ser un número positivo.")
        self._radio=float(validar_radio)  
    
    def calcular_area(self): 
          return math.pi * (self._radio**2)
      
    def calcular_perimetro(self):
          return 2 * math.pi * self._radio

# --- clase hija Rectangulo ---

class Rectangulo(Figura):
    def __init__(self, ancho, alto, nombre):
        super().__init__(nombre)
        self._ancho=None
        self._alto=None
        self.ancho=ancho
        self.alto=alto
    
    @property
    def ancho(self):
        return self._ancho
    
    @ancho.setter
    def ancho(self,validar_ancho):
        if not isinstance(validar_ancho,(int,float)): # Esto es para validar que el ancho sea un numero y no un string
            raise TypeError("El ancho debe ser un número.")
        if  validar_ancho <= 0 : # Y esto para que sea un numero positivo
            raise ValueError("El ancho debe ser un número positivo.") 
        self._ancho = float(validar_ancho)
    
    @property
    def alto(self):
        return self._alto
    
    @alto.setter
    def alto(self,validar_alto):
        if not isinstance(validar_alto,(int,float)):
            raise TypeError("El alto debe ser un número.")
        if validar_alto <= 0:
            raise ValueError("El alto debe ser un número positivo.")
        self._alto = float(validar_alto)
    
    def calcular_area(self):
        return self._ancho * self._alto
    
    def calcular_perimetro(self):
        return 2 * (self._ancho + self._alto)
    
# --- Funcionalidad Polimórfica ---

lista_figuras = [
    Circulo(5,"circulo de jose"),
    Circulo(10,"circulo de paulo"),
    Circulo(7.5,"Órbita de Sabiduría"),
    Circulo(100,"Rueda de la Vida"),
    
    Rectangulo(3,4,"Rectangulo de jose"),
    Rectangulo(6,4,"El Espejo Perfecto"),
    Rectangulo(7.5,5.3,"Rectángulo Fantástico"),
    Rectangulo(2,10,"El Reino de los Lados"),
]

for Figura in lista_figuras:
    Figura.mostrar_info()
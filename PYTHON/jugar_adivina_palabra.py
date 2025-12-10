import random


def jugar_adivina_palabra():
    """
    Juego de consola donde el jugador adivina una palabra secreta.
    """
    lista_palabras = ["python", "programar", "codigo", "desarrollo", "computadora", "aprendizaje"]
    palabra_secreta = random.choice(lista_palabras).lower()
    intentos_maximos = 6
    intentos_restantes = intentos_maximos
    letras_adivinadas = set()
    palabra_mostrada = ["_"] * len(palabra_secreta)
    juego_terminado = False


    print("¡Bienvenido al Juego Adivina la Palabra!")
    print(f"La palabra tiene {len(palabra_secreta)} letras.")


    while not juego_terminado and intentos_restantes > 0:
        print("\n" + " ".join(palabra_mostrada))  
        print(f"Intentos restantes: {intentos_restantes}")
        print(f"Letras adivinadas: {', '.join(sorted(list(letras_adivinadas)))}")


        while True:
            intento = input("Ingresa una letra: ").lower()
            if len(intento) == 1 and intento.isalpha():
                break
            else:
                print("Por favor, ingresa una sola letra válida.")


        if intento in letras_adivinadas:
            print("Ya intentaste esa letra. ¡Intenta otra!")
            continue


        letras_adivinadas.add(intento)


        if intento in palabra_secreta:
            print("¡Correcto!")
            for i, letra in enumerate(palabra_secreta):
                if letra == intento:
                    palabra_mostrada[i] = intento
            if "".join(palabra_mostrada) == palabra_secreta:
                juego_terminado = True
                print("\n¡Felicidades! ¡Adivinaste la palabra:", palabra_secreta + "!")
        else:
            intentos_restantes -= 1
            print(f"¡Incorrecto! La letra '{intento}' no está en la palabra.")


        if intentos_restantes == 0 and not juego_terminado:
            juego_terminado = True
            print("\n¡Se acabaron los intentos! La palabra secreta era:", palabra_secreta)


if __name__ == "__main__":
    jugar_adivina_palabra()
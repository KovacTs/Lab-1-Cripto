def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():  # Solo desplaza letras
            base = ord('A') if caracter.isupper() else ord('a')
            resultado += chr((ord(caracter) - base + desplazamiento) % 26 + base)
        else:
            resultado += caracter  # No cambia espacios, números o signos
    return resultado


if __name__ == "__main__":
    texto = input("Ingrese el texto a cifrar: ")
    desplazamiento = int(input("Ingrese el desplazamiento: "))
    cifrado = cifrado_cesar(texto, desplazamiento)
    print(f"Texto cifrado: {cifrado}")

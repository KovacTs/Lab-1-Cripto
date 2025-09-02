#!/usr/bin/env python3
from scapy.all import IP, ICMP, send
import time

# Función de cifrado César
def cifrado_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():  # Solo desplaza letras
            base = ord('A') if caracter.isupper() else ord('a')
            resultado += chr((ord(caracter) - base + desplazamiento) % 26 + base)
        else:
            resultado += caracter  # No cambia espacios, números o signos
    return resultado

# Función para enviar el texto por ICMP, un carácter por paquete
def enviar_icmp_string(destino, mensaje):
    for i, caracter in enumerate(mensaje):
        paquete = IP(dst=destino)/ICMP(type=8)/bytes(caracter, "utf-8")
        print(f"[+] Enviando carácter {i+1}/{len(mensaje)}: '{caracter}' -> {destino}")
        send(paquete, verbose=0)
        time.sleep(0.2)  # pequeña pausa para no saturar

if __name__ == "__main__":
    destino = input("Ingrese la dirección IP destino: ")
    texto = input("Ingrese el texto a enviar: ")
    desplazamiento = int(input("Ingrese el desplazamiento para el cifrado César: "))

    # Cifrar el texto antes de enviarlo
    texto_cifrado = cifrado_cesar(texto, desplazamiento)
    print(f"[+] Texto cifrado: {texto_cifrado}")

    # Enviar el texto cifrado
    enviar_icmp_string(destino, texto_cifrado)

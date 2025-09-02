#!/usr/bin/env python3
from scapy.all import sniff, ICMP
import string

# Función para descifrado César
def descifrado_cesar(texto, desplazamiento):
    resultado = ""
    for caracter in texto:
        if caracter.isalpha():
            base = ord('A') if caracter.isupper() else ord('a')
            resultado += chr((ord(caracter) - base - desplazamiento) % 26 + base)
        else:
            resultado += caracter
    return resultado

# Función para detectar la "mejor opción" basada en la cantidad de letras imprimibles
def puntuacion(texto):
    return sum(1 for c in texto if c in string.ascii_letters or c.isspace())

# Captura los caracteres de los paquetes ICMP
def capturar_mensaje(iface=None, timeout=15):
    mensaje = []

    def procesar_paquete(paquete):
        if ICMP in paquete and paquete[ICMP].type == 8:  # Echo Request
            payload = bytes(paquete[ICMP].payload).decode(errors='ignore')
            mensaje.append(payload)

    print(f"[+] Capturando paquetes ICMP durante {timeout} segundos...")
    sniff(filter="icmp", prn=procesar_paquete, iface=iface, timeout=timeout)
    return "".join(mensaje)

if __name__ == "__main__":
    # Opcional: especificar la interfaz de red
    iface = input("Ingrese la interfaz para capturar paquetes (enter para default): ") or None
    mensaje_recibido = capturar_mensaje(iface)

    print(f"[+] Mensaje recibido (cifrado): {mensaje_recibido}")

    mejores_puntajes = []
    for desplazamiento in range(26):
        posible_texto = descifrado_cesar(mensaje_recibido, desplazamiento)
        score = puntuacion(posible_texto)
        mejores_puntajes.append((score, desplazamiento, posible_texto))

    # Ordenar por puntaje (mejor opción primero)
    mejores_puntajes.sort(reverse=True, key=lambda x: x[0])
    mejor_opcion = mejores_puntajes[0]

    # Imprimir todas las opciones
    for score, desplazamiento, texto in mejores_puntajes:
        if texto == mejor_opcion[2]:
            # Verde para la opción más probable
            print(f"\033[92mDesplazamiento {desplazamiento}: {texto}\033[0m")
        else:
            print(f"Desplazamiento {desplazamiento}: {texto}")


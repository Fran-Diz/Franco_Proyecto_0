def separar_viento(campo_viento: str) -> tuple:
    """Convierte un campo de viento como 'Norte  3' en (direccion, velocidad).
    Contempla el caso 'Calma' (sin velocidad numérica)."""
    
    partes = campo_viento.strip().split()
     # Si solo hay una palabra (ej. "Calma")
    if len(partes) == 1:
        return (partes[0], 0)
    # La última parte es siempre la velocidad, y el resto es la dirección
    velocidad = partes[-1]
    direccion = " ".join(partes[:-1])
    # Convertir la velocidad a número si es posible
    try:
        velocidad = float(velocidad)
        if velocidad.is_integer():
            velocidad = int(velocidad)
    except ValueError:
        pass
        
    return (direccion, velocidad)


def leer_observaciones(ruta: str) -> tuple:
    """Lee el archivo de observaciones del SMN y devuelve una tupla
    (observaciones, lineas_invalidas), donde observaciones es un diccionario
    {ciudad: datos} con los nombres de ciudad limpios y el campo de viento
    ya separado en dirección y velocidad, y lineas_invalidas es la cantidad
    de líneas que no tenían los 10 campos esperados."""

    observaciones = {}
    lineas_invalidas = 0

    with open(ruta, encoding="latin-1") as archivo:
        for linea in archivo:
            campos = linea.strip().split(";")
            
            # si no son 10 campos, es inválida
            if len(campos) != 10:
                lineas_invalidas += 1
                continue
            
            # limpio nombre de la ciudad (campos[0])
            ciudad = campos[0].strip()
            
            # Separamos el viento usando tu función
            direccion_viento, velocidad_viento = separar_viento(campos[8])
            
            # armo el diccionario interno con los demás campos ya separados
            datos = {
                "fecha": campos[1].strip(),
                "hora": campos[2].strip(),
                "condicion": campos[3].strip(),
                "visibilidad": campos[4].strip(),
                "temperatura": campos[5].strip(),
                "sensacion_termica": campos[6].strip(),
                "humedad": campos[7].strip(),
                "direccion_viento": direccion_viento,
                "velocidad_viento": velocidad_viento,
                "presion": campos[9].strip()
            }
            
            # Lo guardo en 'observaciones' usando la ciudad como clave
            observaciones[ciudad] = datos

    return observaciones, lineas_invalidas


def cantidad_ciudades(observaciones: dict) -> int:
    """Devuelve la cantidad total de ciudades leídas."""
    return len(observaciones)


def cantidad_ciudades_completas(observaciones: dict) -> int:
    """Devuelve la cantidad de ciudades cuya sensación térmica se calcula."""
    contador = 0
    for datos in observaciones.values():
        if datos["sensacion_termica"] != "No se calcula":
            contador += 1
    return contador


def top_n_ciudades(observaciones: dict, campo: str, n: int, descendente: bool = True) -> list:
    """Devuelve las n (por parámetro) ciudades ordenadas según 'campo', de mayor a menor
    (o al revés si descendente=False), en una lista. Reutilizable tanto para temperatura
    como para viento."""
    
    def obtener_valor(elemento):
        return elemento[1]

    lista_datos = []
    for ciudad, datos in observaciones.items():
        valor_str = datos[campo]
        try:
            valor = float(valor_str)
            lista_datos.append((ciudad, valor))
        except ValueError:
            continue
            
    lista_datos.sort(key=obtener_valor, reverse=descendente)
    
    top_n = [item[0] for item in lista_datos[:n]]
    
    return top_n


if __name__ == "__main__":
    observaciones, lineas_invalidas = leer_observaciones("datos/observaciones_smn.txt")

    print("Cantidad total de ciudades:", cantidad_ciudades(observaciones))
    print("Ciudades completas:", cantidad_ciudades_completas(observaciones))
    print("Líneas inválidas:", lineas_invalidas)

    print("\nTop 5 ciudades más cálidas:")
    print(top_n_ciudades(observaciones, "temperatura", 5, descendente=True))
    
    print("\nTop 5 ciudades con más viento:")
    print(top_n_ciudades(observaciones, "velocidad_viento", 5, descendente=True))
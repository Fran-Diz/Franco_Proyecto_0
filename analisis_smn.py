def separar_viento(campo_viento: str) -> tuple:
    """Convierte un campo de viento como 'Norte  3' en (direccion, velocidad).
    Contempla el caso 'Calma' (sin velocidad numérica)."""
    
    partes = campo_viento.strip().split()
    
    # Si solo hay una palabra (ej. "Calma")
    if len(partes) == 1:
        return (partes[0], None)  #0 
    
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


def leer_observaciones(ruta: str) -> dict:
    """Lee el archivo de observaciones del SMN y devuelve un diccionario
    {ciudad: datos}, con los nombres de ciudad limpios y el campo de viento
    ya separado en dirección y velocidad."""

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

    return observaciones


if __name__ == "__main__":
    observaciones = leer_observaciones("datos/observaciones_smn.txt")
    print(observaciones["Bahía Blanca"])
    print(len(observaciones))
    
    print("\nPruebas aisladas de separar_viento:")
    print(separar_viento("Oeste  7"))
    print(separar_viento("Calma"))
    print(separar_viento("Direcciones Variables  11"))



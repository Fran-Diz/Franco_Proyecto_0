import sys
import json
from datetime import datetime

COLUMNAS_ESPERADAS = [
    "ciudad", "fecha", "hora", "condicion", "visibilidad",
    "temperatura", "sensacion_termica", "humedad", "viento", "presion"
]


def separar_viento(campo_viento: str) -> tuple:
    """Convierte un campo de viento como 'Norte  3' en (direccion, velocidad).
    Contempla el caso 'Calma', que se representa como velocidad 0 (no como
    dato faltante, porque calma es información real sobre el viento)."""
    
    partes = campo_viento.strip().split()

    # campo de viento vacío: no hay dirección ni velocidad
    if len(partes) == 0:
        return ("", "")

    # caso "Calma", no hay velocidad
    if len(partes) == 1:
        return (partes[0], 0)

    # la última parte es la velocidad, el resto es la dirección
    velocidad = partes[-1]
    direccion = " ".join(partes[:-1])

    # convierto a número si se puede
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
    {ciudad: datos} con los nombres de ciudad limpios, fecha_y_hora unificada
    como datetime.datetime, temperatura como float, y el campo de viento ya
    separado en dirección y velocidad. lineas_invalidas cuenta las líneas
    descartadas, ya sea por tener una cantidad de campos incorrecta, por
    tener fecha/hora mal formada, o por tener una temperatura no numérica."""

    # para pasar el nombre del mes a número
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }

    observaciones = {}
    lineas_invalidas = 0

    with open(ruta, encoding="latin-1") as archivo:
        for linea in archivo:
            campos = linea.strip().split(";")

            # si no son 10 campos, la línea está mal
            if len(campos) != 10:
                lineas_invalidas += 1
                continue

            # limpio el nombre de la ciudad
            ciudad = campos[0].strip()

            # armo la fecha y hora juntas
            try:
                partes_fecha = campos[1].strip().split("-")
                dia = int(partes_fecha[0])
                mes = meses[partes_fecha[1].lower()]
                anio = int(partes_fecha[2])

                partes_hora = campos[2].strip().split(":")
                hora = int(partes_hora[0])
                minuto = int(partes_hora[1])

                fecha_y_hora = datetime(anio, mes, dia, hora, minuto)
            except (ValueError, KeyError, IndexError):
                # fecha u hora mal escrita, descarto la línea
                lineas_invalidas += 1
                continue

            # paso la temperatura a número
            try:
                temperatura = float(campos[5].strip())
            except ValueError:
                lineas_invalidas += 1
                continue

            # separo el viento en dirección y velocidad
            direccion_viento, velocidad_viento = separar_viento(campos[8])

            # armo el diccionario con todos los datos de la ciudad
            datos = {
                "fecha_y_hora": fecha_y_hora,
                "condicion": campos[3].strip(),
                "visibilidad": campos[4].strip(),
                "temperatura": temperatura,
                "sensacion_termica": campos[6].strip(),  # puede ser "No se calcula"
                "humedad": campos[7].strip(),
                "direccion_viento": direccion_viento,
                "velocidad_viento": velocidad_viento,
                "presion": campos[9].strip()  # todavía tiene el " /" sucio
            }

            observaciones[ciudad] = datos

    return observaciones, lineas_invalidas


def cantidad_ciudades(observaciones: dict) -> int:
    """Devuelve la cantidad total de ciudades leídas."""
    return len(observaciones)


def cantidad_ciudades_completas(observaciones: dict) -> int:
    """Devuelve la cantidad de ciudades sin ningún dato faltante.
    velocidad_viento en 0 (caso 'Calma') no cuenta como faltante,
    porque es información real."""
    # uso datos_faltantes_por_campo para no repetir el mismo chequeo
    incompletas = []

    for ciudades in datos_faltantes_por_campo(observaciones).values():
        for ciudad in ciudades:
            if ciudad not in incompletas:  # para no contarla dos veces
                incompletas.append(ciudad)

    return len(observaciones) - len(incompletas)


def top_n_ciudades(observaciones: dict, campo: str, n: int, descendente: bool = True) -> list:
    """Devuelve las n (por parámetro) ciudades ordenadas según 'campo', de mayor a menor
    (o al revés si descendente=False), en una lista. Reutilizable tanto para temperatura
    como para viento."""

    # Uso sort
    def obtener_valor(elemento):
        return elemento[1]

    # armo lista de (ciudad, valor) descartando lo que no sea número
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


def datos_faltantes_por_campo(observaciones: dict) -> dict:
    """Devuelve un diccionario {campo: [ciudades donde falta ese campo]}.
    Se considera dato faltante el valor 'No se calcula', que es el único
    caso real de dato faltante que aparece en el archivo del SMN."""
    valores_faltantes = ["No se calcula"]
    faltantes = {}

    for ciudad, datos in observaciones.items():
        for campo, valor in datos.items():
            if valor in valores_faltantes:
                if campo not in faltantes:  # primera vez que aparece este campo
                    faltantes[campo] = []
                faltantes[campo].append(ciudad)

    return faltantes


def campos_ausentes(ruta: str) -> dict:
    """Detecta qué columnas esperadas no están presentes en cada línea del archivo.
    Devuelve {numero_de_linea: [columnas ausentes]}, solo para las líneas a las
    que les falta algo. Se asume que las columnas que faltan son las últimas,
    porque el archivo tiene un orden fijo separado por ';'."""
    # recibe la ruta y no 'observaciones' porque leer_observaciones ya
    # descarta estas líneas, entonces hay que leer el archivo de nuevo
    ausentes = {}

    with open(ruta, encoding="latin-1") as archivo:
        for numero_linea, linea in enumerate(archivo, start=1):
            linea = linea.strip()

            if linea == "":  # línea vacía, no cuenta
                continue

            campos = linea.split(";")
            cantidad = len(campos)

            if cantidad < len(COLUMNAS_ESPERADAS):
                ausentes[numero_linea] = COLUMNAS_ESPERADAS[cantidad:]

    return ausentes


def ciudades_extremo(observaciones: dict, campo: str, maximo: bool = True) -> list:
    """Devuelve la lista de ciudades con el valor máximo (o mínimo si maximo=False)
    de 'campo'. Si hay empate devuelve todas. Ignora valores no numéricos.
    Reutilizable para temperatura y velocidad de viento."""
    valor_extremo = None
    ciudades = []

    for ciudad, datos in observaciones.items():
        try:
            valor = float(datos[campo])
        except (ValueError, TypeError):
            continue

        if valor_extremo is None:
            es_nuevo_extremo = True
        elif maximo:
            es_nuevo_extremo = valor > valor_extremo
        else:
            es_nuevo_extremo = valor < valor_extremo

        if es_nuevo_extremo:
            # valor más extremo, arranco lista nueva
            valor_extremo = valor
            ciudades = [ciudad]
        elif valor == valor_extremo:
            # empate, la sumo a la lista
            ciudades.append(ciudad)

    return ciudades

def horarios_reportados(observaciones: dict) -> list:
    """Devuelve la lista de horarios "HH:MM" a los que reportaron las estaciones,
    sin repetir y ordenados de menor a mayor."""
    horarios = []

    for datos in observaciones.values():
        hora = datos["fecha_y_hora"].hour
        minuto = datos["fecha_y_hora"].minute

        # agrego un 0 adelante si tiene un solo dígito (8 -> "08")
        texto_hora = str(hora)
        if hora < 10:
            texto_hora = "0" + texto_hora

        texto_minuto = str(minuto)
        if minuto < 10:
            texto_minuto = "0" + texto_minuto

        horario = texto_hora + ":" + texto_minuto

        if horario not in horarios:  # para no repetir
            horarios.append(horario)

    horarios.sort()
    return horarios


def mostrar_resumen(observaciones: dict, lineas_invalidas: int, ausentes: dict) -> None:
    """Imprime por pantalla el resumen con todas las características calculadas. Usar n=5"""
    n = 5
    
    print("      RESUMEN DE OBSERVACIONES METEOROLÓGICAS (SMN)")

    print(f" Cantidad total de ciudades leídas: {cantidad_ciudades(observaciones)}")
    print(f" Ciudades con datos completos: {cantidad_ciudades_completas(observaciones)}")
    print(f" Líneas inválidas descartadas: {lineas_invalidas}")
    print(f" Horarios reportados: {', '.join(horarios_reportados(observaciones))}")

    if ausentes:
        print(f" Líneas con columnas faltantes: {len(ausentes)}")
    else:
        print(" No se detectaron líneas con columnas faltantes.")

    print("\n Extremos ")

    ciudades = ciudades_extremo(observaciones, "temperatura", True)
    if ciudades:
        valor = observaciones[ciudades[0]]["temperatura"]
        print(f"  Temperatura máxima: {valor} °C ({', '.join(ciudades)})")

    ciudades = ciudades_extremo(observaciones, "temperatura", False)
    if ciudades:
        valor = observaciones[ciudades[0]]["temperatura"]
        print(f"  Temperatura mínima: {valor} °C ({', '.join(ciudades)})")

    ciudades = ciudades_extremo(observaciones, "velocidad_viento", True)
    if ciudades:
        valor = observaciones[ciudades[0]]["velocidad_viento"]
        print(f"  Viento máximo: {valor} km/h ({', '.join(ciudades)})")

    ciudades = ciudades_extremo(observaciones, "velocidad_viento", False)
    if ciudades:
        valor = observaciones[ciudades[0]]["velocidad_viento"]
        print(f" Viento mínimo: {valor} km/h ({', '.join(ciudades)})")

    print("\n Datos faltantes por campo ")
    faltantes = datos_faltantes_por_campo(observaciones)
    if not faltantes:
        print("  Ninguno")
    for campo, ciudades in faltantes.items():
        print(f"   {campo}: {len(ciudades)} ({', '.join(ciudades)})")

    if ausentes:
        print("\n Columnas ausentes por línea ")
        for numero_linea, columnas in ausentes.items():
            print(f"   Línea {numero_linea}: faltan {', '.join(columnas)}")

    print(f"\n Top {n} Ciudades más cálidas ")
    for ciudad in top_n_ciudades(observaciones, "temperatura", n, descendente=True):
        temp = observaciones[ciudad]["temperatura"]
        print(f"   {ciudad}: {temp} °C")

    print(f"\n Top {n} Ciudades más frías ")
    for ciudad in top_n_ciudades(observaciones, "temperatura", n, descendente=False):
        temp = observaciones[ciudad]["temperatura"]
        print(f"   {ciudad}: {temp} °C")

    print(f"\n Top {n} Ciudades con más viento ")
    for ciudad in top_n_ciudades(observaciones, "velocidad_viento", n, descendente=True):
        vel = observaciones[ciudad]["velocidad_viento"]
        dir_v = observaciones[ciudad]["direccion_viento"]
        print(f"   {ciudad}: {vel} km/h ({dir_v})")

    print(f"\n Top {n} Ciudades con menos viento ")
    for ciudad in top_n_ciudades(observaciones, "velocidad_viento", n, descendente=False):
        vel = observaciones[ciudad]["velocidad_viento"]
        dir_v = observaciones[ciudad]["direccion_viento"]
        print(f"   {ciudad}: {vel} km/h ({dir_v})")


if __name__ == "__main__":
    # si no me pasan la ruta como argumento, aviso y corto
    if len(sys.argv) != 2:
        print("Uso: python analisis_smn.py <ruta_del_archivo>")
        print("Ejemplo: python analisis_smn.py datos/observaciones_smn.txt")
        sys.exit(1)

    ruta = sys.argv[1]

    try:
        observaciones, lineas_invalidas = leer_observaciones(ruta)
        ausentes = campos_ausentes(ruta)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{ruta}'.")
        sys.exit(1)

    # el archivo abrió bien pero no había ninguna observación válida
    if not observaciones:
        if lineas_invalidas == 0:
            print(f"Error: el archivo '{ruta}' está vacío.")
        else:
            print(f"Error: '{ruta}' no tiene observaciones válidas "
                  f"({lineas_invalidas} líneas inválidas).")
        sys.exit(1)


    mostrar_resumen(observaciones, lineas_invalidas, ausentes)
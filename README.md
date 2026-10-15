# Analisis del clima proyecto 0.1

 Proyecto 0.1- Franco Diz Díaz

Programa que lee el archivo de observaciones actuales del Servicio Meteorológico
Nacional, guarda los datos en un diccionario (una clave por ciudad), lo convierte
a JSON y muestra un resumen con estadísticas.

## Cómo conseguir el archivo

1. Entrar a https://www.smn.gob.ar/descarga-de-datos
2. Bajar el `.rar` de observaciones actuales y descomprimirlo.
3. Copiar el `.txt` a la carpeta `datos/` con el nombre `observaciones_smn.txt`.

Los datos son en vivo, así que cada vez que se descarga da algo distinto.

## Cómo ejecutarlo

El programa recibe un solo parámetro, la ruta del archivo, y hace cosas
distintas según qué se le pase (en Linux se usa `python3`):

```bash
python analisis_smn.py datos/observaciones_smn.txt
python analisis_smn.py obs_json/observaciones_smn.json
python analisis_smn.py
```

- **Archivo `.txt` del SMN:** detecta si está en `utf-8` o `latin-1`, lo convierte
  a JSON (con la fecha en formato ISO 8601 sin segundos) y lo guarda en
  `obs_json/` con el mismo nombre (si la carpeta no existe, la crea). Va
  imprimiendo una leyenda antes de cada paso, después la cantidad de ciudades
  contenidas e informadas, y por último el resumen completo.
- **Archivo `.json`:** imprime la cantidad de ciudades contenidas e informadas.
- **Sin parámetros:** avisa e informa cuántos `.txt` hay en `datos/` y cuántos
  `.json` hay en `obs_json/`.
- **Más de un parámetro:** avisa y termina sin hacer nada más.

Si el archivo no existe, no es `.txt` ni `.json`, o no tiene observaciones
válidas, avisa con un mensaje y termina.

## Cómo funciona

Lo que hace `leer_observaciones` es cortar cada línea por `;`, revisar que tenga
10 campos y pasar la fecha, la temperatura y el viento a los tipos que necesito.
Con eso arma un diccionario de diccionarios:

```python
{"Azul": {"fecha_y_hora": ..., "temperatura": 3.3, "velocidad_viento": 5, ...}}
```

`detectar_y_leer_txt` prueba abrir el archivo con `utf-8` y, si falla, usa
`latin-1`. `procesar_archivo_txt` convierte el diccionario a JSON y lo guarda, y
`procesar_archivo_json` lee un JSON ya guardado.

Después el resto de las funciones recorren el diccionario para contar ciudades,
buscar datos faltantes, sacar máximos y mínimos, armar los rankings y listar los
horarios. `mostrar_resumen` solo imprime lo que devuelven.

Algunas decisiones que tomé:

- **Ciudades contenidas:** el total de ciudades del archivo.
- **Ciudades informadas:** las que tienen todos sus datos completos (sin ningún
  `No se calcula`).
- `Calma` queda como dirección "Calma" y velocidad 0, porque es un dato real.
- `No se calcula` en sensación térmica cuenta como dato faltante.
- Las líneas con otra cantidad de campos, con fecha mal escrita o con temperatura
  que no es número se descartan y se cuentan como inválidas.
- `campos_ausentes` vuelve a leer el archivo porque esas líneas ya no están en el
  diccionario.
- La carpeta `obs_json/` se genera al correr el programa, por eso está en el
  `.gitignore`.

## Ejemplo de salida por consola

Corriendo `python analisis_smn.py datos/observaciones_smn.txt` con el archivo de
ejemplo:

```
archivo del SMN, convirtiendo a json...
archivo del SMN, detectando codificación...
codificación detectada: latin-1, leyendo observaciones...
el directorio obs_json no existe, creándolo...
guardando archivo en obs_json/observaciones_smn.json...
conversión completada.
Ciudades contenidas: 121
Ciudades informadas: 25

      RESUMEN DE OBSERVACIONES METEOROLÓGICAS (SMN)
 Cantidad total de ciudades leídas: 121
 Ciudades con datos completos: 25
 Líneas inválidas descartadas: 0
 Horarios reportados: 09:00, 10:00, 11:00, 12:00, 13:00, 15:00
 No se detectaron líneas con columnas faltantes.

 Extremos 
  Temperatura máxima: 28.0 °C (Rivadavia)
  Temperatura mínima: -28.6 °C (Base Belgrano II)
  Viento máximo: 42 km/h (Mount Pleasant Airport (Islas Malvinas))
 Viento mínimo: 0 km/h (Bolívar, Mar del Plata, Olavarría, Pigué, Villa María Del Río Seco, Uspallata, Cipolletti, Metán, Rivadavia, Gobernador Gregores, Base Carlini)

 Datos faltantes por campo 
   sensacion_termica: 96 (Azul, Bahía Blanca, Benito Juárez, ...)

 Top 5 Ciudades más cálidas 
   Rivadavia: 28.0 °C
   Orán: 27.4 °C
   Pcia. Roque Saenz Peña: 26.7 °C
   Tartagal: 26.4 °C
   Resistencia: 26.3 °C

 Top 5 Ciudades más frías 
   Base Belgrano II: -28.6 °C
   Base San Martín: -24.8 °C
   Base Orcadas: -24.3 °C
   Base Marambio: -15.5 °C
   Base Esperanza: -9.5 °C

 Top 5 Ciudades con más viento 
   Mount Pleasant Airport (Islas Malvinas): 42 km/h (Sur)
   Perito Moreno: 38 km/h (Este)
   Río Gallegos: 37 km/h (Sudoeste)
   San Julián: 37 km/h (Sudoeste)
   Comodoro Rivadavia: 33 km/h (Sur)

 Top 5 Ciudades con menos viento 
   Bolívar: 0 km/h (Calma)
   Mar del Plata: 0 km/h (Calma)
   Olavarría: 0 km/h (Calma)
   Pigué: 0 km/h (Calma)
   Villa María Del Río Seco: 0 km/h (Calma)
```

Con un `.json` la salida es solo esto:

```
leyendo archivo JSON: obs_json/observaciones_smn.json...
Ciudades contenidas: 121
Ciudades informadas: 25
```

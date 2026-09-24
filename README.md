#Analisis del clima proyecto 0
# Análisis de observaciones del SMN

Programa que lee el archivo de observaciones actuales del Servicio Meteorológico
Nacional, guarda los datos en un diccionario (una clave por ciudad) y muestra un
resumen con estadísticas.


## Cómo ejecutarlo

```bash
python analisis_smn.py datos/observaciones_smn.txt
```

Si no se pasa el archivo, no existe o está vacío, avisa con un mensaje y termina.

## Cómo funciona

Lo que hace `leer_observaciones` es cortar cada línea por `;`, revisar que tenga
10 campos y pasar la fecha, la temperatura y el viento a los tipos que necesito.
Con eso arma un diccionario de diccionarios:

```python
{"Azul": {"fecha_y_hora": ..., "temperatura": 3.3, "velocidad_viento": 5, ...}}
```

Después el resto de las funciones recorren ese diccionario para contar ciudades,
buscar datos faltantes, sacar máximos y mínimos, armar los rankings y listar los
horarios. `mostrar_resumen` solo imprime lo que devuelven.

Algunas decisiones que tomé:

- `Calma` queda como dirección "Calma" y velocidad 0, porque es un dato real.
- `No se calcula` en sensación térmica cuenta como dato faltante.
- Las líneas con otra cantidad de campos, con fecha mal escrita o con temperatura
  que no es número se descartan y se cuentan como inválidas.
- `campos_ausentes` vuelve a leer el archivo porque esas líneas ya no están en el
  diccionario.

## Ejemplo de salida

```text
      RESUMEN DE OBSERVACIONES METEOROLÓGICAS 
- Cantidad total de ciudades leídas: 121
- Ciudades con datos completos: 25
- Líneas inválidas descartadas: 0
- Horarios reportados: 09:00, 10:00, 11:00, 12:00, 13:00, 15:00
- No se detectaron líneas con columnas faltantes.

--- Top 5 Ciudades más cálidas ---
  -> Rivadavia: 28.0 °C
  -> Orán: 27.4 °C
  ...
```
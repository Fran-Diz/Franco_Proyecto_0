# Analisis del clima proyecto 0

 Proyecto 0 - Franco Diz Díaz

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

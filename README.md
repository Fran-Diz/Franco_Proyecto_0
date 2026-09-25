# Analisis del clima proyecto 0

 Proyecto 0 - Franco Diz Díaz

Programa que lee el archivo de observaciones actuales del Servicio Meteorológico
Nacional, guarda los datos en un diccionario (una clave por ciudad) y muestra un
resumen con estadísticas.

## Cómo conseguir el archivo

1. Entrar a https://www.smn.gob.ar/descarga-de-datos
2. Bajar el `.rar` de observaciones actuales y descomprimirlo.
3. Copiar el `.txt` a la carpeta `datos/` con el nombre `observaciones_smn.txt`.

Los datos son en vivo, así que cada vez que se descarga da algo distinto.


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

## Ejemplo de salida por consola

Corriendo `python analisis_smn.py datos/observaciones_smn.txt` con el archivo de
ejemplo:

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
   sensacion_termica: 96 (Azul, Bahía Blanca, Benito Juárez, Bolívar, Campo de Mayo, Coronel Suarez, Dolores, El Palomar, Ezeiza, Junín, La Plata, Las Flores, Mar del Plata, Mariano Moreno, Merlo, Morón, Nueve de Julio, Olavarría, Pehuajó, Pigué, Punta Indio B.A., San Fernando, Tandil, Trenque Lauquen, Tres Arroyos, Villa Gesell, Aeroparque Buenos Aires, Buenos Aires, Catamarca, Tinogasta, Puerto Madryn, Trelew, Córdoba, Córdoba Observatorio, Esc. Aviación Militar, Laboulaye, Marcos Juárez, Pilar Obs., Río Cuarto, Villa Dolores, Villa María Del Río Seco, Corrientes, Ituzaingó, Mercedes, Monte Caseros, Paso De Los Libres, Concordia, Gualeguaychú, Paraná, Formosa, La Quiaca, Jujuy, Jujuy Universidad Nacional, General Pico, Victorica, Santa Rosa, Chamical, Chepes, Chilecito, La Rioja, Malargue, Mendoza, Mendoza Observatorio, San Martín (Mza), San Rafael, Uspallata, Bernardo De Irigoyen, Iguazú, Oberá, Posadas, Neuquén, Cipolletti, El Bolsón, Maquinchao, Río Colorado, Viedma, Metán, Salta, Jachal, San Juan, San Luis, Santa Rosa del Conlara, Villa Reynolds, Gobernador Gregores, Ceres, Rafaela, Reconquista, Rosario, Santa Fe, Sunchales, Venado Tuerto, Termas de Rio Hondo, Santiago del Estero, Tucumán, Base Esperanza, Base Carlini)

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
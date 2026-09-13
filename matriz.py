matriz = [
            [17, 45, 47, 59, 64, 39, 65],
            [22, 97, 66, 52, 8, 70, 74],
            [81, 29, 97, 5, 92, 10, 39],
            [20, 43, 14, 81, 61, 5, 19],
            [35, 44, 33, 14, 52, 31, 53]
            ]

#opcion 1
for sector in matriz:          # Bucle 1: entra a la matriz y toma cada fila/lista
    suma_sector = 0
    cantidad = 0
    
    for valor in sector:        # Bucle 2: recorre los números de esa fila en específico
        if valor != -1:         # Ignoramos las mediciones no registradas (-1)
            suma_sector += valor
            cantidad += 1
            
    if cantidad > 0:
        promedio = suma_sector / cantidad
        print(f"Suma: {suma_sector}, Promedio: {promedio}")
print(matriz)


#forma limpia
for sector in matriz:
    # 1. Filtramos los valores válidos (excluimos el -1)
    validos = [valor for valor in sector if valor != -1] #lista  por comprension, recorre cada valor en la fila y si el valor es diferente de -1 lo agrega a la lista validos
    print
    # 2. Sumamos directamente la lista filtrada
    if validos:
        suma_sector = sum(validos)
        promedio = suma_sector / len(validos)

# Mismo resultado sin lista por comprensión:
validos = []                     # 1. Creas la lista vacía
for valor in sector:             # 2. El for que recorre
    if valor != -1:              # 3. La condición que filtra
        validos.append(valor)    # 4. Lo que guardas en la lista

print(validos)  # Muestra los valores válidos para ese sector
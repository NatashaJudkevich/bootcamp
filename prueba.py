def leer_archivo(archivo):
    datos = []
    registros_erroneos = []
    with open(archivo, "r", encoding="utf-8") as file:
        lineas = file.readlines()
        encabezados = lineas[0].strip().split(",")  # Leer y procesar los encabezados
        for linea in lineas[1:]:
            campos = linea.strip().split(",")
            # Verificar si la cantidad de campos es igual a la de los encabezados
            if len(campos) != len(encabezados):
                campos.append("Inconsistencia en el número de columnas")
                registros_erroneos.append(campos)
            else:
                datos.append(campos)
    return datos, registros_erroneos, encabezados

def guardar_registros_erroneos(registros_erroneos, encabezados, archivo_salida):
    with open(archivo_salida, "w", encoding="utf-8") as file:
        encabezado_completo = ",".join(encabezados) + ",OBSERVACIÓN\n"
        file.write(encabezado_completo)
        for registro in registros_erroneos:
            linea = ",".join(registro) + "\n"
            file.write(linea)

def distribucion_por_genero(datos):
    generos = {"M": 0, "F": 0}
    for fila in datos:
        genero = fila[0]  # Columna 'sexo'
        if genero in generos:
            generos[genero] += 1
    return generos

def vacunas_por_tipo(datos):
    conteo_vacunas = {}
    total_vacunas = len(datos)
    for fila in datos:
        vacuna = fila[11]  # Columna 'vacuna'
        if vacuna not in conteo_vacunas:
            conteo_vacunas[vacuna] = 0
        conteo_vacunas[vacuna] += 1
    return conteo_vacunas, total_vacunas

def dosis_por_jurisdiccion(datos):
    jurisdicciones = {}
    for fila in datos:
        jurisdiccion = fila[2]  # Columna 'jurisdiccion_residencia'
        if jurisdiccion not in jurisdicciones:
            jurisdicciones[jurisdiccion] = 0
        jurisdicciones[jurisdiccion] += 1
    return jurisdicciones

def segunda_dosis_por_jurisdiccion(datos):
    segundas_dosis = {}
    for fila in datos:
        jurisdiccion = fila[2]  # Columna 'jurisdiccion_residencia'
        nombre_dosis = fila[13]  # Columna 'nombre_dosis_generica'
        if nombre_dosis == '2da':
            if jurisdiccion not in segundas_dosis:
                segundas_dosis[jurisdiccion] = 0
            segundas_dosis[jurisdiccion] += 1
    return segundas_dosis

def refuerzos_mayores_60(datos):
    refuerzos = 0
    for fila in datos:
        grupo_etario = fila[1]  # Columna 'grupo_etario'
        nombre_dosis = fila[13]  # Columna 'nombre_dosis_generica'
        if grupo_etario == '60 o más años' and nombre_dosis == 'Refuerzo':
            refuerzos += 1
    return refuerzos

def main():
    archivo = "C:\\Users\\Nash\\Desktop\\BOOTCAMP\\datos_nomivac_parte1.csv"
    datos, registros_erroneos, encabezados = leer_archivo(archivo)
    
    # Guardar registros erróneos en un archivo
    guardar_registros_erroneos(registros_erroneos, encabezados, "registros_erroneos.csv")
    
    # Realizar análisis descriptivo
    generos = distribucion_por_genero(datos)
    vacunas, total_vacunas = vacunas_por_tipo(datos)
    dosis_jurisdiccion = dosis_por_jurisdiccion(datos)
    
    # Pedido especial
    segundas_dosis_jurisdiccion = segunda_dosis_por_jurisdiccion(datos)
    refuerzos_mayores_60_result = refuerzos_mayores_60(datos)
    
    # Imprimir resultados
    print("Distribución por Género:")
    for genero, cantidad in generos.items():
        print(f"{'Masculino' if genero == 'M' else 'Femenino'}: {cantidad}")

    print("\nVacunas Aplicadas por Tipo de Vacuna:")
    for vacuna, cantidad in vacunas.items():
        porcentaje = (cantidad / total_vacunas) * 100
        print(f"{vacuna}: {porcentaje:.2f}%")

    print("\nDosis por Jurisdicción de Residencia:")
    for jurisdiccion, cantidad in dosis_jurisdiccion.items():
        print(f"{jurisdiccion}: {cantidad} dosis")

    print("\nSegundas Dosis por Jurisdicción:")
    for jurisdiccion, cantidad in segundas_dosis_jurisdiccion.items():
        print(f"{jurisdiccion}: {cantidad} segundas dosis")

    print(f"\nPersonas mayores de 60 años con dosis de refuerzo: {refuerzos_mayores_60_result}")

if __name__ == "__main__":
    main()

def leer_archivo(archivo):
    datos = []
    with open(archivo, "r") as archivo:
        for linea in archivo:
            # Dividir la línea en una lista de campos separados por coma
            campos = linea.strip().split(",")
            datos.append(campos)
    return datos

# Leer el archivo
datos = leer_archivo("C:\\Users\\Nash\\Desktop\\BOOTCAMP\\modelo_muestra.csv")

def validar_fila(fila):
    observacion = None
    
    # Validar el campo sexo (índice 0 en la fila)
    if fila[0] not in ['M', 'F']:
        observacion = 'Sexo inválido'
        
    # Validar el campo grupo_etario (índice 1 en la fila)
    if not fila[1].isdigit() and '<' not in fila[1] and '-' not in fila[1]:
        observacion = 'Grupo etario inválido'
    
    # Validar el campo fecha_aplicacion (índice 9 en la fila)
    try:
        año, mes, día = map(int, fila[9].split("-"))
        if not (1 <= mes <= 12 and 1 <= día <= 31):
            observacion = 'Fecha de aplicación inválida'
    except:
        observacion = 'Fecha de aplicación inválida'
    
    return observacion

# Lista para almacenar filas erróneas
errores = []
for fila in datos:
    error = validar_fila(fila)
    if error:
        fila.append(error)
        errores.append(fila)

# Guardar los errores en un archivo CSV
with open("errores.csv", "w", encoding="utf-8") as archivo_errores:
    for error in errores:
        archivo_errores.write(",".join(error) + "\n")


def contar_por_genero(datos):
    conteo = {'M': 0, 'F': 0}
    for fila in datos:
        if fila[0] == 'M':
            conteo['M'] += 1
        elif fila[0] == 'F':
            conteo['F'] += 1
    return conteo

# Calcular el conteo por género
conteo_genero = contar_por_genero(datos)
print(f"Masculino: {conteo_genero['M']}")
print(f"Femenino: {conteo_genero['F']}")


def contar_por_vacuna(datos):
    conteo_vacunas = {}
    total = 0
    for fila in datos:
        vacuna = fila[10]  # índice de la columna 'vacuna'
        if vacuna not in conteo_vacunas:
            conteo_vacunas[vacuna] = 0
        conteo_vacunas[vacuna] += 1
        total += 1
    return conteo_vacunas, total

# Calcular el conteo por tipo de vacuna
conteo_vacunas, total_vacunas = contar_por_vacuna(datos)
for vacuna, cantidad in conteo_vacunas.items():
    proporcion = (cantidad / total_vacunas) * 100
    print(f"{vacuna}: {proporcion:.2f}%")

def dosis_por_jurisdiccion(datos):
    conteo_jurisdiccion = {}
    for fila in datos:
        jurisdiccion = fila[2]  # índice de la columna 'jurisdiccion_residencia'
        if jurisdiccion not in conteo_jurisdiccion:
            conteo_jurisdiccion[jurisdiccion] = 0
        conteo_jurisdiccion[jurisdiccion] += 1
    return conteo_jurisdiccion

# Calcular las dosis por jurisdicción
conteo_jurisdiccion = dosis_por_jurisdiccion(datos)
for jurisdiccion, cantidad in conteo_jurisdiccion.items():
    print(f"{jurisdiccion}: {cantidad} dosis")

def segunda_dosis_por_jurisdiccion(datos):
    conteo_segunda_dosis = {}
    for fila in datos:
        if fila[12] == '2da':  # índice de la columna 'nombre_dosis_generica'
            jurisdiccion = fila[2]  # índice de la columna 'jurisdiccion_residencia'
            if jurisdiccion not in conteo_segunda_dosis:
                conteo_segunda_dosis[jurisdiccion] = 0
            conteo_segunda_dosis[jurisdiccion] += 1
    return conteo_segunda_dosis

# Calcular la segunda dosis por jurisdicción
segunda_dosis_jurisdiccion = segunda_dosis_por_jurisdiccion(datos)
for jurisdiccion, cantidad in segunda_dosis_jurisdiccion.items():
    print(f"{jurisdiccion}: {cantidad} segunda dosis")

def refuerzo_mayores_60(datos):
    conteo_refuerzos = 0
    for fila in datos:
        if fila[1] == '60 o más años' and fila[12] == 'Refuerzo':  # índices de 'grupo_etario' y 'nombre_dosis_generica'
            conteo_refuerzos += 1
    return conteo_refuerzos

# Calcular la cantidad de refuerzos para mayores de 60 años
mayores_60_refuerzos = refuerzo_mayores_60(datos)
print(f"Personas mayores de 60 años con refuerzo: {mayores_60_refuerzos}")
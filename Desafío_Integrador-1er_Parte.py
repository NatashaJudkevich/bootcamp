def leer_archivo(archivo):
    datos = []
    registros_erroneos = []
    with open(archivo, "r", encoding="utf-8") as file:
        lineas = file.readlines()
        encabezados = lineas[0].strip().split(",")  # Lee y procesa los encabezados del archivo 
        for linea in lineas[1:]:
            campos = linea.strip().split(",")
            errores = []
            
            # Verifica si la cantidad de campos es igual a la de los encabezados
            if len(campos) != len(encabezados):
                errores.append("Inconsistencia en el número de columnas")
            else:
                # Valida campo 'sexo' (columna 0)
                if campos[0] not in ['M', 'F']:
                    errores.append("Valor incorrecto en el campo 'sexo'")

                # Valida campo 'grupo_etario' (columna 1)
                if not validar_grupo_etario(campos[1]):
                    errores.append("Formato incorrecto en el campo 'grupo_etario'")

                # Valida campo 'fecha_aplicacion' (columna 10) - formato de fecha
                if not validar_fecha(campos[10]):
                    errores.append("Formato de fecha incorrecto en el campo 'fecha_aplicacion'")

                # Valida campo 'vacuna' (columna 11) - que no este vacío
                if not campos[11]:
                    errores.append("Campo 'vacuna' está vacío")

                # Valida campo 'nombre_dosis_generica' (columna 13) - que sea un valor válido
                dosis_validas = ['1ra', '2da', 'Refuerzo']
                if campos[13] not in dosis_validas:
                    errores.append("Valor incorrecto en el campo 'nombre_dosis_generica'")

            if errores:
                registro_erroneo = campos + ["; ".join(errores)]
                registros_erroneos.append(registro_erroneo)
            else:
                datos.append(campos)
                
    return datos, registros_erroneos, encabezados

def validar_grupo_etario(grupo_etario):
    # Valida que el grupo etario sea de la forma "numero-numero"
    partes = grupo_etario.split("-")
    if len(partes) == 2:
        # Verifico que ambas partes sean numeros enteros
        if partes[0].isdigit() and partes[1].isdigit():
            return True
    return False

def validar_fecha(fecha):
    # Valida si la fecha tiene el formato "YYYY-MM-DD"
    partes = fecha.split("-")
    if len(partes) == 3:
        anio, mes, dia = partes
        # Verifico que el año, mes y dia sean numeros y tengan el tamaño correcto
        if (len(anio) == 4 and anio.isdigit() and 
            len(mes) == 2 and mes.isdigit() and 1 <= int(mes) <= 12 and 
            len(dia) == 2 and dia.isdigit() and 1 <= int(dia) <= 31):
            return True
    return False

def guardar_registros_erroneos(registros_erroneos, encabezados, archivo_salida):
    with open(archivo_salida, "w", encoding="utf-8") as file:
        encabezado_completo = ",".join(encabezados) + ",OBSERVACIÓN\n"
        file.write(encabezado_completo)
        for registro in registros_erroneos:
            registro_limpio = [campo.strip() for campo in registro]
            linea = ",".join(registro_limpio) + "\n"
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
    personas_vistas = set()  # Usaremos un conjunto para almacenar los ids de personas ya contadas

    for fila in datos:
        jurisdiccion = fila[2].strip()  # Columna 'jurisdiccion_residencia'
        id_persona = fila[-1].strip()   # Columna 'id_persona_dw'

        # Verificar si la persona ya fue contada
        if id_persona not in personas_vistas:
            personas_vistas.add(id_persona)  # Marcar a la persona como contada
            
            if jurisdiccion not in jurisdicciones:
                jurisdicciones[jurisdiccion] = 0
            jurisdicciones[jurisdiccion] += 1  # Contar la dosis en la jurisdicción
    return jurisdicciones

def segunda_dosis_por_jurisdiccion(datos):
    segundas_dosis = {}
    for fila in datos:
        jurisdiccion = fila[2].strip()  # Columna 'jurisdiccion_residencia'
        nom_dosis_generica = fila[13].strip()  # Columna 'cod_dosis_generica'
        
        # Verificar si el codigo de dosis es '2da' para identificar segundas dosis
        if nom_dosis_generica == '2da':
            if jurisdiccion not in segundas_dosis:
                segundas_dosis[jurisdiccion] = 0
            segundas_dosis[jurisdiccion] += 1
    return segundas_dosis

def refuerzos_mayores_60(datos):
    refuerzos = 0
    for fila in datos:
        grupo_etario = fila[1].strip().lower()
        cod_dosis_generica = fila[12].strip()
        
        # Verifico si el codigo de dosis es '3' (refuerzo) y si el grupo etario es de mayores de 60 años
        if cod_dosis_generica == '3':
            # Extraigo el primer numero del rango de edad
            rango_edad = grupo_etario.split('-')
            if len(rango_edad) == 2 and rango_edad[0].isdigit():
                edad_minima = int(rango_edad[0])

                # Verifico si la edad minima es 60 o más
                if edad_minima >= 60:
                    refuerzos += 1

    return refuerzos

def main():
    archivo = "Z:\\Documentos\\Edgardo\\Python\\Ecom\\TP Integrador 1\\datos_nomivac_parte1.csv"
    datos, registros_erroneos, encabezados = leer_archivo(archivo)
    
    # Guarda registros erroneos en un archivo
    guardar_registros_erroneos(registros_erroneos, encabezados, "erroneos.csv")
    
    # Realiza analisis descriptivo
    generos = distribucion_por_genero(datos)
    vacunas, total_vacunas = vacunas_por_tipo(datos)
    dosis_jurisdiccion = dosis_por_jurisdiccion(datos)
    
    # Pedido especial
    segundas_dosis_jurisdiccion = segunda_dosis_por_jurisdiccion(datos)
    refuerzos_mayores_60_result = refuerzos_mayores_60(datos)
    
    # Imprime resultados
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
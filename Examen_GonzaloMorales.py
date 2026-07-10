planes = {
    "F001": ["Plan Basico", "mensual", 1, False, False, "Libre"],
    "F002": ["Plan Full", "mensual", 1, True, True, "Libre"],
    "F003": ["Plan Estudiante", "trimestral", 3, False, True, "Tarde"],
    "F004": ["Plan Senior", "trimestral", 3, True, False, "Mañana"],
    "F005": ["Plan Anual Pro", "anual", 12, True, True, "Libre"],
    "F006": ["Plan Nocturno", "mensual", 1, False, True, "Noche"]
}
inscripciones = {
    "F001": [14990, 30],
    "F002": [22900, 10],
    "F003": [39990, 0],
    "F004": [35990, 6],
    "F005": [159990, 2],
    "F006": [18990, 15]
}

#FUNCIONES VALIDACIÓN
def val_len(entrada):
    validacion = input(entrada).strip()
    if len(validacion) == 0:
        return False
    else:
        return validacion.lower()
    
def num_positivo(entrada):
    try:
        numero = int(input(entrada))
        if numero < 0:
            return False
        else:
            return numero
    except ValueError:
        return False

def buscar_codigo(codigo, planes):
    codigo = codigo.upper()
    for clave in planes:
        if clave.upper() == codigo:
            return True
    return False

def validar_codigo(codigo, planes, inscripciones):
    if codigo.strip() == "":
        return False
    if buscar_codigo(codigo, planes) or buscar_codigo(codigo, inscripciones):
        return False
    return True

def val_nombre(nombre):
    return nombre.strip() != ""

def tipo_plan(tipo):
    return tipo.lower() in ("mensual", "trimestral", "anual")

def val_duracion(duracion):
    try:
        return int(duracion) > 0
    except ValueError:
        return False

def val_acceso_piscina(valor):
    return valor.lower() in ("s", "n")

def val_incluye_clases(valor):
    return valor.lower() in ("s", "n")

def val_horario(horario):
    return horario.strip() != ""

def val_precio(precio):
    try:
        return int(precio) > 0
    except ValueError:
        return False
 
def val_cupos(cupos):
    try:
        return int(cupos) >= 0
    except ValueError:
        return False

#FUNCIONES MENÚ PRINCIPAL
def cupos_tipos(tipo_plan, planes, inscripciones):
    cupos_totales = 0
    if tipo_plan in ["mensual", "anual", "trimestral"]:
        for plan in planes:
            if planes[plan][1] == tipo_plan:
                cupos_totales += inscripciones[plan][1]
        print(f"El total de cupos disponibles para el tipo de plan {tipo_plan} es: {cupos_totales}")
    else:
        print("Tipo de plan inválido. Por favor, ingresa mensual, trimestral o anual.")

def busqueda_precio(p_min, p_max, planes, inscripciones):
    planes_precio = []
    for inscripcion in inscripciones:
        if inscripciones[inscripcion][0] >= p_min and inscripciones[inscripcion][0] <= p_max and inscripciones[inscripcion][1] != 0:
            for plan in planes:
                if inscripcion == plan:
                    planes_agregados = (f"{planes[plan][0]}-{plan}")
                    planes_precio.append((planes_agregados))

    if len(planes_precio) == 0:
        print("No hay planes en ese rango de precios.")
    else:
        planes_precio.sort()
        print(f"Los planes encontrados son: {planes_precio}")

def actualizar_precio(codigo, nuevo_precio, planes, inscripciones):
    if buscar_codigo(codigo, planes):
        for clave in inscripciones:
            if clave.upper() == codigo.upper():
                inscripciones[clave][0] = nuevo_precio
                return True
    return False

def agregar_plan(codigo, nombre, tipo, duracion, acceso_piscina, incluye_clases, horario, precio, cupos, planes, inscripciones):
    if buscar_codigo(codigo, planes) or buscar_codigo(codigo, inscripciones):
        return False
 
    planes[codigo] = [nombre, tipo.lower(), int(duracion),
                       acceso_piscina.lower() == "s",
                       incluye_clases.lower() == "s",
                       horario]
    inscripciones[codigo] = [int(precio), int(cupos)]
    return True

def eliminar_plan(codigo, planes, inscripciones):
    if buscar_codigo(codigo, planes):
        for clave in list(planes.keys()):
            if clave.upper() == codigo.upper():
                del planes[clave]
                del inscripciones[clave]
                return True
    return False

#MENÚ
def mostrar_menú():
    print("======MENÚ PRINCIPAL FITPASS=====")
    print("1. Cupos por tipo de plan\n" \
    "2. Búsqueda de planes por rango de precio\n" \
    "3. Actualizar precio de plan\n" \
    "4. Agregar plan\n" \
    "5. Eliminar plan\n" \
    "6. Salir")

def leer_opcion():
    try:
        opcion = int(input("Ingrese opción: "))
        if opcion in [1,2,3,4,5,6]:
            return opcion
        else:
            return False
    except ValueError:
        return None

def main():
    while True:
        mostrar_menú()
        op = leer_opcion()
        if op == 1:
            tipo = val_len("Ingrese el tipo de plan a buscar(mensual, trimestral o anual): ")
            cupos_tipos(tipo, planes, inscripciones)
        elif op == 2:
            while True:
                p_min = num_positivo("Ingrese el valor mínimo de búsqueda: ")
                if p_min is False:
                    print("Debe ingresar valores válidos para el rango de precios.")
                    continue

                p_max = num_positivo("Ingrese el valor máximo de búsqueda: ")
                if p_max is False:
                    print("Debe ingresar valores válidos para el rango de precios.")
                    continue

                if p_min > p_max:
                    print("El precio mínimo debe ser menor al precio máximo.")
                    continue

                busqueda_precio(p_min, p_max, planes, inscripciones)
                break
        elif op == 3:
            while True:
                codigo = input("Ingrese código del plan: ")
                try:
                    nuevo_precio = int(input("Ingrese nuevo precio: "))
                except ValueError:
                    print("Debe ingresar un valor entero para el precio")
                    continue
 
                if actualizar_precio(codigo, nuevo_precio, planes, inscripciones):
                    print("Precio actualizado")
                else:
                    print("El código no existe")
 
                repetir = input("¿Desea actualizar otro precio (s/n)?: ")
                if repetir.lower() != "s":
                    break
        elif op == 4:
            codigo = input("Ingrese código del plan: ")
            nombre = input("Ingrese nombre del plan: ")
            tipo = input("Ingrese tipo (mensual/trimestral/anual): ")
            duracion = input("Ingrese duración (meses): ")
            acceso_piscina = input("¿Incluye acceso a piscina? (s/n): ")
            incluye_clases = input("¿Incluye clases grupales? (s/n): ")
            horario = input("Ingrese horario: ")
            precio = input("Ingrese precio: ")
            cupos = input("Ingrese cupos: ")
 
            if not validar_codigo(codigo, planes, inscripciones):
                print("El código no es válido o ya existe")
            elif not val_nombre(nombre):
                print("El nombre no es válido")
            elif not tipo_plan(tipo):
                print("El tipo debe ser 'mensual', 'trimestral' o 'anual'")
            elif not val_duracion(duracion):
                print("La duración debe ser un número entero mayor que cero")
            elif not val_acceso_piscina(acceso_piscina):
                print("El acceso a piscina debe ser 's' o 'n'")
            elif not val_incluye_clases(incluye_clases):
                print("La inclusión de clases debe ser 's' o 'n'")
            elif not val_horario(horario):
                print("El horario no es válido")
            elif not val_precio(precio):
                print("El precio debe ser un número entero mayor que cero")
            elif not val_cupos(cupos):
                print("Los cupos deben ser un número entero mayor o igual a cero")
            else:
                agregado = agregar_plan(codigo, nombre, tipo, duracion, acceso_piscina,
                                         incluye_clases, horario, precio, cupos,
                                         planes, inscripciones)
                if agregado:
                    print("Plan agregado")
                else:
                    print("El código ya existe")
        elif op == 5:
            codigo = input("Ingrese código del plan a eliminar: ")
            if eliminar_plan(codigo, planes, inscripciones):
                print("Plan eliminado")
            else:
                print("El código no existe")
        elif op == 6:
            break
        else:
            print("Ingresa un valor dentro del rango 1-6. Intente nuevamente.")

main()
print("Programa finalizado.")
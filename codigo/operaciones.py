from datos import NOMBRE_SECTORES
from datos import DIAS_SEMANA
from datos import mostrar_matriz

# Validación de datos--------------------------------------------------------------------(nicky)
def validar_sector(sector):
   if (sector.isnumeric() and int(sector) in range(len(NOMBRE_SECTORES))):
       return True
   else:
       return False

def validar_dia(dia):
   if (dia.isnumeric() and int(dia) in range(len(DIAS_SEMANA))):
       return True
   else:
       return False

def validar_humedad(humedad):
   if (humedad.isnumeric() and int(humedad) in range(-1, 101)):
       return True
   else:
       return False

def registrar_medicion(valores_actuales):

    try:
        id_sector = input("Ingrese el numero de sector: ")
        while not validar_sector(id_sector):
            print("Sector inválido")
            id_sector = input("Ingrese el numero de sector: ")

        id_dia = input("Ingrese el numero de dia, siendo 0 = Lunes, 6 = Domingo: ")
        while not validar_dia(id_dia):
            print("Día inválido")
            id_dia = input("Ingrese el numero de dia, siendo 0 = Lunes, 6 = Domingo: ")

        humedad = input("Ingrese la humedad: ")
        while not validar_humedad(humedad):
            print("Humedad inválida")
            humedad = input("Ingrese la humedad: ")

        if valores_actuales[int(id_sector)][int(id_dia)] != -1:
            raise ValueError("Ese valor ya fue registrado")

        valores_actuales[int(id_sector)][int(id_dia)] = int(humedad)

        return valores_actuales

    except ValueError as error:
        print(f"Error: {error}")
        return valores_actuales

#Funciones seccion Priscila--------------------------------------------------------------------(priscila)
# funcion que devuelvve 1 sector en especifico, lo indica el usuario
def getValuesPerSector(sector_id):
    if not validar_sector(sector_id):
            id_sector = input("Ingrese el numero de sector: ")
            while not validar_sector(id_sector): #si el sector ingresado no es valido, se le vuelve a pedir al usuario que ingrese un sector valido
                print("Sector inválido")
                id_sector = input("Ingrese el numero de sector: ")
    return datos[sector_id]

#def ordenHumidityValues(sector_id):


#-----------------------------------------------------------------------------------

#Opciones del menú--------------------------------------------------------------------(nicky)
def menu(valores_actuales):
    while True:
        opcion = input("¿Qué desea hacer? (1 = Ver matriz de humedad / 2 = Registrar medición / 3 = Obtener valores de un sector / fin = Salir): ").strip().lower()

        match opcion:
            case "fin":
                break
            case "1":
                mostrar_matriz(valores_actuales)
            case "2":
                registrar_medicion(valores_actuales)
            case "3":
                # Llamar a la función para obtener los valores de un sector específico
                getValuesPerSector(valores_actuales)
            case _:
                print("Opción inválida")
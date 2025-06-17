from datetime import datetime

class Paciente:
    def __init__(self, nombre, dni, fecha_nacimiento):

        self.__nombre = nombre.strip()
        self.__dni = dni.strip()
        self.__fecha_nacimiento = fecha_nacimiento.strip()
  
    def obtener_dni(self):
        return self.__dni
    
    def __str__(self):
        return f"Paciente: {self.__nombre}, DNI: {self.__dni}, Nacimiento: {self.__fecha_nacimiento}"
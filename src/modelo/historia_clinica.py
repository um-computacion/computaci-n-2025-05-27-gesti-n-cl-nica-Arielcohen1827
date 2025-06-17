from .paciente import Paciente
from .turno import Turno
from .receta import Receta

class HistoriaClinica:
    def __init__(self, paciente):
        if paciente is None:
            raise ValueError("El paciente no debe ser None")
        if not isinstance(paciente, Paciente):
            raise ValueError("Debe proporcionar un paciente valido")
        
        self.__paciente = paciente
        self.__turnos = []
        self.__recetas = []

    def agregar_turno(self, turno):
        if turno is None:
            raise ValueError("El turno no puede ser None")
        if not isinstance(turno, Turno):
            raise ValueError("Debe proporcionar un turno valido")
        
        self.__turnos.append(turno)

    def agregar_receta(self, receta):
        if receta is None:
            raise ValueError("La receta no debe ser None")
        if not isinstance(receta, Receta):
            raise ValueError("Debe proporcionar una Receta valida")
        
        self.__recetas.append(receta)
    
    def obtener_turnos(self):
        return self.__turnos.copy()
    
    def obtener_recetas(self):
        return self.__recetas.copy()
    
    def __str__(self):
        nombre_paciente = str(self.__paciente).split(':')[1].split(',')[0].strip()

        resultado = f"Historia Clinica de {nombre_paciente}\n"
        resultado += "=" * 50 + "\n"

        resultado += f"Turnos ({len(self.__turnos)}):\n"
        if self.__turnos:
            for i, turno in enumerate(self.__turnos, 1):
                resultado += f"{i}. {turno}\n"
        else:
            resultado += "No hay turnos registrados\n"

        resultado += "\n"

        resultado += f"Recetas ({len(self.__recetas)}):\n"
        if self.__recetas:
            for i, receta in enumerate(self.__recetas, 1):
                resultado += f"{i}. {receta}\n"
        else:
            resultado += "No hay recetas registradas\n"

        return resultado
            
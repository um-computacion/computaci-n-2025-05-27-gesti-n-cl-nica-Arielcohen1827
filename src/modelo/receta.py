from datetime import datetime

class Receta:
    def __init__(self, paciente, medico, medicamentos):
            
        self.__paciente = paciente
        self.__medico = medico 
        self.__medicamentos = [med.strip() for med in medicamentos]
        self.__fecha = datetime.now()

    def __str__(self):
        fecha_str = self.__fecha.strftime("%d/%m/%Y %H:%M")
        medicamentos_str = ", ".join(self.__medicamentos)

        nombre_paciente = str(self.__paciente).split(':')[1].split(',')[0].strip()
        nombre_medico = str(self.__medico).split(',')[0].replace("Dr. ", "").strip()

        return (f"Receta - Paciente: {nombre_paciente}"
                f" - Medico: Dr. {nombre_medico}"
                f" - Medicamentos: {medicamentos_str}"
                f" - Fecha: {fecha_str}")
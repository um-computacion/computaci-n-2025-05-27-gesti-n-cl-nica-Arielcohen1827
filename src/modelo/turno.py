
class Turno:
    def __init__(self, paciente, medico, fecha_hora, especialidad):
        
        self.__paciente = paciente
        self.__medico = medico
        self.__fecha_hora = fecha_hora
        self.__especialidad = especialidad.strip()
    
    def obtener_paciente(self):
        return self.__paciente

    def obtener_medico(self):
        return self.__medico
    
    def obtener_fecha_hora(self):
        return self.__fecha_hora
    
    def __str__(self):
        fecha_str = self.__fecha_hora.strftime("%d/%m/%Y %H:%M")
        return (f"Turno: {self.__paciente.obtener_dni()} ({str(self.__paciente).split(':')[1].split(',')[0].strip()}) "
                f"con {str(self.__medico).split(',')[0]} "
                f"- Especialidad: {self.__especialidad} "
                f"- Fecha: {fecha_str}")
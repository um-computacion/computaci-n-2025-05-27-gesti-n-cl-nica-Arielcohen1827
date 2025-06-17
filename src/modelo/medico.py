
from .especialidad import Especialidad

class Medico:
    def __init__(self, nombre, matricula):
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del medico no debe estar vacio")
        if not matricula or not matricula.strip():
            raise ValueError("La matricula no debe estar vacia")
        
        self.__nombre = nombre.strip()
        self.__matricula = matricula.strip()
        self.__especialidades = []

    def agregar_especialidad(self, especialidad):
        if not isinstance(especialidad, Especialidad):
            raise ValueError("Debe proporcionar una especialidad valida")

        nueva_especialidad = especialidad.obtener_especialidad()
        nuevos_dias = especialidad._Especialidad__dias  # acceso interno a los días

        for esp_existente in self.__especialidades:
            # 1. Misma especialidad ya registrada
            if esp_existente.obtener_especialidad() == nueva_especialidad:
                raise ValueError(f"La especialidad {nueva_especialidad} ya está registrada para este médico.")

            # 2. Días en conflicto con otra especialidad
            dias_existentes = esp_existente._Especialidad__dias
            for dia in nuevos_dias:
                if dia in dias_existentes:
                    raise ValueError(
                        f"Conflicto de días: El día '{dia}' ya está asignado a la especialidad "
                        f"{esp_existente.obtener_especialidad()} del mismo médico."
                    )

        self.__especialidades.append(especialidad)

    def obtener_especialidad_para_dia(self, dia):
        for especialidad in self.__especialidades:
            if especialidad.verificar_dia(dia):
                return especialidad.obtener_especialidad()
            
        return None
    
    def obtener_matricula(self):
        return self.__matricula
    
    def __str__(self):
        especialidades_str = ""
        if self.__especialidades:
            nombres_esp = [esp.obtener_especialidad() for esp in self.__especialidades]
            especialidades_str = f" - Especialidades: {', '.join(nombres_esp)}"
        return f"Dr. {self.__nombre}, Matricula: {self.__matricula}{especialidades_str}"

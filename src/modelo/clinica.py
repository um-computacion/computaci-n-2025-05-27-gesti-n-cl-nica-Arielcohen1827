from datetime import datetime
from .paciente import Paciente
from .medico import Medico
from .turno import Turno
from .receta import Receta
from .historia_clinica import HistoriaClinica
from .excepciones import (
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException
) 

class Clinica:
    def __init__(self):
        self.__pacientes = {}
        self.__medicos = {}
        self.__turnos = []
        self.__historias_clinicas = {}

    # Pacientes

    def agregar_paciente(self, paciente):
        if not isinstance(paciente, Paciente):
            raise ValueError("Debe proporcionar un Paciente valido")
        
        dni = paciente.obtener_dni()

        if dni in self.__pacientes:
            raise ValueError(f"Ya existe un paciente con DNI: {dni}")
        
        self.__pacientes[dni] = paciente
        self.__historias_clinicas[dni] = HistoriaClinica(paciente)

    def obtener_pacientes(self):
        return list(self.__pacientes.values())
    
    def validar_existencia_paciente(self, dni):
        if dni not in self.__pacientes:
            raise PacienteNoEncontradoException(f"No se encontro el paciente con DNI: {dni}")
        
    # Medicos

    def agregar_medico(self, medico):
        if not isinstance(medico, Medico):
            raise ValueError("Debe proporcionar un Medico valido")
        
        matricula = medico.obtener_matricula()

        if matricula in self.__medicos:
            raise ValueError(f"Ya existe el medico con matricula: {matricula}")
        
        self.__medicos[matricula] = medico

    def obtener_medicos(self):
        return list(self.__medicos.values())
    
    def obtener_medico_por_matricula(self, matricula):
        if matricula not in self.__medicos:
            raise MedicoNoEncontradoException(f"No se encontro medico con matricula: {matricula}")
        
        return self.__medicos[matricula]
    
    def validar_existencia_medico(self, matricula):
        if matricula not in self.__medicos:
            raise MedicoNoEncontradoException(f"No se encontro medico con matricula: {matricula}")
        
    # Turnos

    def agendar_turno(self, dni, matricula, especialidad, fecha_hora):
        self.validar_existencia_paciente(dni)
        paciente = self.__pacientes[dni]

        self.validar_existencia_medico(matricula)
        medico = self.__medicos[matricula]

        self.validar_fecha_no_pasada(fecha_hora)

        dia_semana = self.obtener_dia_semana_español(fecha_hora)
        
        self.validar_especialidad_en_dia(medico, especialidad, dia_semana)

        self.validar_turno_no_duplicado(matricula, fecha_hora)

        turno = Turno(paciente, medico, fecha_hora, especialidad)
        self.__turnos.append(turno)

        self.__historias_clinicas[dni].agregar_turno(turno)

    def obtener_turnos(self):
        return self.__turnos.copy()
    
    def validar_turno_no_duplicado(self, matricula, fecha_hora):
        for turno in self.__turnos:
            if (turno.obtener_medico().obtener_matricula() == matricula and
                 turno.obtener_fecha_hora() == fecha_hora):
                raise TurnoOcupadoException(f"El medico ya tiene un turno agendado en {fecha_hora}")

    def obtener_dia_semana_español(self, fecha_hora):
        dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
        return dias[fecha_hora.weekday()]
    
    def validar_fecha_no_pasada(self, fecha_hora):
        if fecha_hora < datetime.now():
            fecha_str = fecha_hora.strftime("%d/%m/%Y %H:%M")
            raise ValueError(f"No se puede agendar un turno en el pasado: {fecha_str}")

    def validar_especialidad_en_dia(self, medico, especialidad_solicitada, dia_semana):
        especialidad_disponible = medico.obtener_especialidad_para_dia(dia_semana)
        
        if especialidad_disponible is None:
            raise MedicoNoDisponibleException(
                f"El medico no atiende los {dia_semana}"
            )
        
        if especialidad_disponible.lower() != especialidad_solicitada.lower():
            raise MedicoNoDisponibleException(
                f"El medico no atiende {especialidad_solicitada} los dias {dia_semana}\n"
                f"Atiende: {especialidad_disponible}"
            )
        
    # Recetas
    
    def emitir_receta(self, dni, matricula, medicamentos):
        self.validar_existencia_paciente(dni)
        paciente = self.__pacientes[dni]

        self.validar_existencia_medico(matricula)
        medico = self.__medicos[matricula]

        medicamentos_limpios = [m.strip() for m in medicamentos if m.strip()]

        if not medicamentos_limpios:
            raise RecetaInvalidaException("Debe haber al menos un medicamento válido")
            
        receta = Receta(paciente, medico, medicamentos)
        
        self.__historias_clinicas[dni].agregar_receta(receta)

    # Historias Clinicas
    
    def obtener_historia_clinica(self, dni):
        self.validar_existencia_paciente(dni)
        return self.__historias_clinicas[dni]
    
    def obtener_medicos_por_especialidad(self, especialidad: str):
        medicos_filtrados = []
        for medico in self.__medicos.values():
            # Por ejemplo si medico.especialidades es una lista
            if especialidad.lower() in [esp.lower() for esp in medico.especialidades]:
                medicos_filtrados.append(medico)
        return medicos_filtrados

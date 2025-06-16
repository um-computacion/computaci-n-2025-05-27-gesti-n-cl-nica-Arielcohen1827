class PacienteNoEncontradoException(Exception):
    """Excepción lanzada cuando no se encuentra un paciente."""
    def __init__(self, dni):
        super().__init__(f"Paciente con DNI {dni} no encontrado.")

class MedicoNoEncontradoException(Exception):
    """Excepción lanzada cuando no se encuentra un médico."""
    def __init__(self, matricula):
        super().__init__(f"Médico con matrícula {matricula} no encontrado.")

class MedicoNoDisponibleException(Exception):
    """Excepción lanzada cuando un médico no está disponible."""
    def __init__(self, matricula):
        super().__init__(f"Médico con matrícula {matricula} no disponible.")


class TurnoOcupadoException(Exception):
    """Excepción lanzada cuando un turno ya está ocupado."""
    def __init__(self, fecha_hora):
        super().__init__(f"Turno ya ocupado para la fecha y hora: {fecha_hora}.")


class RecetaInvalidaException(Exception):
    """Excepción lanzada cuando una receta es inválida."""
    def __init__(self, mensaje="La receta es inválida o no se puede emitir."):
        super().__init__(mensaje)
        
class EspecialidadNoDisponibleError(Exception):
    """Excepción lanzada cuando una especialidad no está disponible."""
    def __init__(self, especialidad):
        super().__init__(f"La especialidad '{especialidad}' no está disponible.")

import unittest
from datetime import datetime
from src.modelo.paciente import Paciente
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad
from src.modelo.clinica import Clinica
from src.modelo.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException
)

class TestClinica(unittest.TestCase):
    
    def setUp(self):
        self.clinica = Clinica()
        
        # Crear pacientes y médicos de prueba
        self.paciente1 = Paciente("Kimi Antonelli", "12345678", "25/08/2006")
        self.paciente2 = Paciente("Franco Colapinto", "87654321", "27/05/2003")
        
        self.medico1 = Medico("Dr. Liam Lawson ", "12345")
        self.pediatria = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])
        self.medico1.agregar_especialidad(self.pediatria)
        
        # Fecha de prueba
        self.fecha_lunes = datetime(2025, 11 , 10, 14, 30)
    
    # Tests pacientes
    
    def test_agregar_paciente(self):
        self.clinica.agregar_paciente(self.paciente1)
        
        pacientes = self.clinica.obtener_pacientes()
        self.assertEqual(len(pacientes), 1)
        self.assertEqual(pacientes[0].obtener_dni(), "12345678")
    
    def test_paciente_duplicado(self):
        self.clinica.agregar_paciente(self.paciente1)
        
        paciente_duplicado = Paciente("Yuki Tsunoda Duplicado", "12345678", "11/05/2000")
        with self.assertRaises(ValueError):
            self.clinica.agregar_paciente(paciente_duplicado)
    
    # Tests medicos
    
    def test_agregar_medico(self):
        self.clinica.agregar_medico(self.medico1)
        
        medicos = self.clinica.obtener_medicos()
        self.assertEqual(len(medicos), 1)
        self.assertEqual(medicos[0].obtener_matricula(), "12345")
    
    def test_medico_duplicado(self):
        self.clinica.agregar_medico(self.medico1)
        
        medico_duplicado = Medico("Dr. Liam Lawson Duplicado", "12345")
        with self.assertRaises(ValueError):
            self.clinica.agregar_medico(medico_duplicado)
    
    # Tests especialidades
    
    def test_agregar_especialidad(self):
        self.clinica.agregar_medico(self.medico1)
        cardiologia = Especialidad("Cardiología", ["martes", "jueves"])
        
        medico = self.clinica.obtener_medico_por_matricula("12345")
        medico.agregar_especialidad(cardiologia)
        
        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Cardiología")
    
    def test_error_agregar_especialidad(self):
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.obtener_medico_por_matricula("33333")
    
    # Tests turnos
    
    def test_agendar_turno_exitoso(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        self.clinica.agendar_turno("12345678", "12345", "Pediatría", self.fecha_lunes)
        
        turnos = self.clinica.obtener_turnos()
        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0].obtener_medico().obtener_matricula(), "12345")
    
    def test_turno_duplicado(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_paciente(self.paciente2)
        self.clinica.agregar_medico(self.medico1)
        
        self.clinica.agendar_turno("12345678", "12345", "Pediatría", self.fecha_lunes)
        
        with self.assertRaises(TurnoOcupadoException):
            self.clinica.agendar_turno("87654321", "12345", "Pediatría", self.fecha_lunes)
    
    def test_error_turno_fecha_pasada(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_pasada = datetime(2024, 1, 1, 10, 0)
        
        with self.assertRaises(ValueError) as context:
            self.clinica.agendar_turno("12345678", "12345", "Pediatría", fecha_pasada)
        
        self.assertIn("pasado", str(context.exception).lower())

    def test_error_turno_paciente_inexistente(self):
        self.clinica.agregar_medico(self.medico1)
        
        with self.assertRaises(PacienteNoEncontradoException):
            self.clinica.agendar_turno("37115932", "12345", "Pediatría", self.fecha_lunes)
    
    def test_error_turno_medico_inexistente(self):
        self.clinica.agregar_paciente(self.paciente1)
        
        with self.assertRaises(MedicoNoEncontradoException):
            self.clinica.agendar_turno("12345678", "33333", "Pediatría", self.fecha_lunes)
    
    def test_error_medico_no_trabaja_ese_dia(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        fecha_martes = datetime(2025, 6, 17, 14, 30)  # Martes
        with self.assertRaises(MedicoNoDisponibleException):
            self.clinica.agendar_turno("12345678", "12345", "Pediatría", fecha_martes)
    
    # Tests recetas
    
    def test_emitir_receta(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        self.clinica.emitir_receta("12345678", "12345", ["Paracetamol 500mg"])
        
        historia = self.clinica.obtener_historia_clinica("12345678")
        recetas = historia.obtener_recetas()
        self.assertEqual(len(recetas), 1)
    
    def test_error_receta_sin_medicamentos(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)

        with self.assertRaises(RecetaInvalidaException):
            self.clinica.emitir_receta("12345678", "12345", [])
    
    # Tests historia clinica
    
    def test_historia_clinica_guarda_correctamente(self):
        self.clinica.agregar_paciente(self.paciente1)
        self.clinica.agregar_medico(self.medico1)
        
        self.clinica.agendar_turno("12345678", "12345", "Pediatría", self.fecha_lunes)
        self.clinica.emitir_receta("12345678", "12345", ["Aspirina 100mg"])
        
        historia = self.clinica.obtener_historia_clinica("12345678")
        self.assertEqual(len(historia.obtener_turnos()), 1)
        self.assertEqual(len(historia.obtener_recetas()), 1)


if __name__ == "__main__":
    unittest.main()
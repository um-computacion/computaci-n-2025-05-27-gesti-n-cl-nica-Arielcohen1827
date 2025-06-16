import unittest
from datetime import datetime
from src.modelo.paciente import Paciente
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad
from src.modelo.turno import Turno
class TestTurno(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Pepito Juan", "12345678", "17/07/1977")
        self.medico = Medico("Dr. Juan Pepito", "MAT11111")
        self.pediatria = Especialidad("Pediatria", ["lunes", "miercoles", "viernes"])
        self.medico.agregar_especialidad(self.pediatria)
        self.fecha_hora = datetime(2025, 6, 16, 14, 30)

    def test_crear_turno(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, "Pediatria")

        self.assertEqual(turno.obtener_medico(), self.medico)
        self.assertEqual(turno.obtener_fecha_hora(), self.fecha_hora)
        self.assertEqual(turno.obtener_paciente(), self.paciente)

    def test_str_representacion(self):
        turno = Turno(self.paciente, self.medico, self.fecha_hora, "Pediatria")
        resultado = str(turno)

        self.assertIn("Pepito Juan", resultado)
        self.assertIn("Dr. Juan Pepito", resultado)
        self.assertIn("Pediatria", resultado)
        self.assertIn("16/06/2025 14:30", resultado)

if __name__ == "__main__":
    unittest.main()
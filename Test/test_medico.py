
import unittest
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad

class TestMedico(unittest.TestCase):

    def setUp(self): #Configuracion inicial para los tests
        self.pediatria = Especialidad("Pediatria", ["lunes", "miercoles", "viernes"])
        self.cardiologia = Especialidad("Cardiologia", ["martes", "jueves"])

    def test_crear_medico(self):
        medico = Medico("Dr. Lance Stroll", "12345")

        self.assertEqual(medico.obtener_matricula(), "12345")
        self.assertIn("Dr. Lance Stroll", str(medico))
        self.assertIn("12345", str(medico))

    def test_agregar_especialidad(self):
        medico = Medico("Dr. Lance Stroll", "12345")

        medico.agregar_especialidad(self.pediatria)
        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Pediatria")
        self.assertIn("Pediatria", str(medico))
    
    def test_duplicados_especialidad(self):
        medico = Medico("Dr. Esteban Ocon", "67891")

        medico.agregar_especialidad(self.pediatria)
        with self.assertRaises(ValueError):
            medico.agregar_especialidad(self.pediatria)

    def test_especialidad_para_dia_disponible(self):
        medico = Medico("Dr. Fernando Alonso", "11111")
        medico.agregar_especialidad(self.pediatria)
        medico.agregar_especialidad(self.cardiologia)

        self.assertEqual(medico.obtener_especialidad_para_dia("lunes"), "Pediatria")
        self.assertEqual(medico.obtener_especialidad_para_dia("martes"), "Cardiologia")
        self.assertIsNone(medico.obtener_especialidad_para_dia("sabado"))

    def test_nombre_vacio(self):
        with self.assertRaises(ValueError):
            Medico("", "77777")

    def test_matricula_vacia(self):
        with self.assertRaises(ValueError):
            Medico("Dr. Lando Norris", "")

    def test_str_(self):
        medico = Medico("Dr. Sergio Pérez", "56556")
        medico.agregar_especialidad(self.pediatria)
        resultado = str(medico)

        self.assertIn("Dr. Sergio Pérez", resultado)
        self.assertIn("56556", resultado)
        self.assertIn("Pediatria", resultado)

if __name__ == "__main__":
    unittest.main()

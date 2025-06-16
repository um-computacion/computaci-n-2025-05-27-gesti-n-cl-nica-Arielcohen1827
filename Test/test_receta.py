import unittest
from datetime import datetime, timedelta
from src.modelo.receta import Receta
from src.modelo.paciente import Paciente
from src.modelo.medico import Medico

class TestReceta(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Pepito Juan", "87654321", "20/05/1985")
        self.medico = Medico("Dr. Juan Pepito", "99999")
        self.medicamentos = ["Paracetamol 500mg", "Ibuprofeno 400mg"]

    def test_crear_receta_valida(self):
        receta = Receta(self.paciente, self.medico, self.medicamentos)
        resultado = str(receta)
        self.assertIn("Pepito Juan", resultado)
        self.assertIn("Dr. Juan Pepito", resultado)
        self.assertIn("Paracetamol 500mg", resultado)
        self.assertIn("Ibuprofeno 400mg", resultado)
        self.assertIsInstance(receta._Receta__fecha, datetime)

    def test_medicamentos_con_espacios(self):
        receta = Receta(self.paciente, self.medico, ["  Ibuprofeno 400mg  "])
        self.assertIn("Ibuprofeno 400mg", str(receta))

    def test_medicamentos_vacios_no_lanzan_error(self):
        receta = Receta(self.paciente, self.medico, [])
        resultado = str(receta)
        self.assertIn("Medicamentos: ", resultado)

    def test_medicamentos_none_lanza_error_tipo(self):
        # Esto lanza error de tipo por intentar iterar sobre None, no por validación
        with self.assertRaises(TypeError):
            Receta(self.paciente, self.medico, None)

    def test_paciente_none_str_falla(self):
        receta = Receta(None, self.medico, self.medicamentos)
        with self.assertRaises(IndexError):
            _ = str(receta)

    def test_medico_none_str_contenido(self):
        receta = Receta(self.paciente, None, self.medicamentos)
        resultado = str(receta)
        self.assertIn("Dr. None", resultado)



    def test_str_formato_general(self):
        receta = Receta(self.paciente, self.medico, self.medicamentos)
        resultado = str(receta)
        self.assertIn("Receta - Paciente: Pepito Juan", resultado)
        self.assertIn(" - Medico: Dr. Juan Pepito", resultado)
        self.assertIn(" - Medicamentos: Paracetamol 500mg, Ibuprofeno 400mg", resultado)
        self.assertRegex(resultado, r"\d{2}/\d{2}/\d{4} \d{2}:\d{2}")

if __name__ == "__main__":
    unittest.main()
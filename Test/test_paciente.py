import unittest
from src.modelo.paciente import Paciente

class TestPaciente(unittest.TestCase):

    def test_crear_paciente_valido(self):
        paciente = Paciente("George Russell", "12345678", "15/02/1998")
        self.assertEqual(paciente.obtener_dni(), "12345678")
        self.assertIn("George Russell", str(paciente))
        self.assertIn("12345678", str(paciente))
        self.assertIn("01/01/1990", str(paciente))

    def test_datos_con_espacios_son_limpiados(self):
        paciente = Paciente("  Ana Gómez  ", "  98765432  ", " 02/02/1985 ")
        self.assertEqual(paciente.obtener_dni(), "98765432")
        self.assertIn("Ana Gómez", str(paciente))
        self.assertNotIn("  ", str(paciente))  # No deben quedar dobles espacios

    def test_str_formato_correcto(self):
        paciente = Paciente("Carlos López", "11122333", "15/03/1975")
        resultado = str(paciente)
        self.assertTrue(resultado.startswith("Paciente: "))
        self.assertIn("Carlos López", resultado)
        self.assertIn("DNI: 11122333", resultado)
        self.assertIn("Nacimiento: 15/03/1975", resultado)

    def test_paciente_con_campos_vacios(self):
        paciente = Paciente("", "", "")
        self.assertEqual(paciente.obtener_dni(), "")
        texto = str(paciente)
        self.assertIn("Paciente: ", texto)
        self.assertIn("DNI: ", texto)
        self.assertIn("Nacimiento: ", texto)

    def test_dni_numerico_con_letras(self):
        """El constructor no valida el formato del DNI, pero el test documenta ese comportamiento."""
        paciente = Paciente("Pedro", "ABC1234", "01/01/2000")
        self.assertEqual(paciente.obtener_dni(), "ABC1234")
        self.assertIn("ABC1234", str(paciente))

    def test_nombre_solo_espacios(self):
        paciente = Paciente("     ", "44444444", "01/01/1995")
        self.assertIn("Paciente: ", str(paciente))  # Mostrará nombre vacío tras strip
        self.assertIn("44444444", str(paciente))


if __name__ == "__main__":
    unittest.main()

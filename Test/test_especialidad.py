import unittest
from src.modelo.especialidad import Especialidad

class TestEspecialidad(unittest.TestCase):

    def test_crear_especialidad(self):
        esp = Especialidad("Pediatria", ["lunes", "miercoles", "viernes"])
        self.assertEqual(esp.obtener_especialidad(), "Pediatria")
        self.assertTrue(esp.verificar_dia("lunes"))
        self.assertTrue(esp.verificar_dia("MIERCOLES"))
        self.assertFalse(esp.verificar_dia("martes"))



    def test_dias_invalidos(self):
        with self.assertRaises(ValueError):
            Especialidad("Cardiologia", ["lunez", "martes"])   
               

    def test_dia_case_insensitive(self):
        esp = Especialidad("Neurologia", ["martes", "jueves"])
        for variante in ["martes", "MARTES", "Martes", "mArTeS"]:
            self.assertTrue(esp.verificar_dia(variante))

    def test_normalizacion_dias_entrada(self):
        esp1 = Especialidad("Neurología", ["miércoles", "sábado"])
        esp2 = Especialidad("Oftalmología", ["miercoles", "sabado"])  
        for dia in ["miercoles", "miércoles", "sabado", "sábado"]:
            self.assertTrue(esp1.verificar_dia(dia))
            self.assertTrue(esp2.verificar_dia(dia))

    def test_normaliza_y_evita_duplicados_equivalentes(self):
        """Si se pasa el mismo día con y sin tilde, solo debe guardarse una vez."""
        esp = Especialidad("Trauma", ["miércoles", "miercoles"])
        
        dias_guardados = esp._Especialidad__dias
        self.assertEqual(dias_guardados.count("miércoles") + dias_guardados.count("miercoles"), 1)


    def test_tipo_se_ajusta_espacios(self):
        esp = Especialidad("  Traumatologia  ", ["lunes"])
        self.assertEqual(esp.obtener_especialidad(), "Traumatologia")

    def test_tipo_vacio_se_permite(self):
        """La implementación actual NO lanza error si el tipo está vacío."""
        esp = Especialidad("", ["lunes"])
        self.assertEqual(esp.obtener_especialidad(), "")


    def test_especialidad_acentos(self):
        esp = Especialidad("Pediatría", ["lunes", "miércoles", "viernes"])
        self.assertEqual(esp.obtener_especialidad(), "Pediatría")
        self.assertTrue(esp.verificar_dia("miércoles"))
        self.assertIn("Pediatría", str(esp))

    def test_str(self):
        esp = Especialidad("Traumatologia", ["lunes", "miercoles"])
        resultado = str(esp)
        self.assertIn("Traumatologia", resultado)
        self.assertIn("lunes", resultado)
        self.assertIn("miercoles", resultado)


if __name__ == "__main__":
    unittest.main()
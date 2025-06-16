import unittest
from datetime import datetime
from src.modelo.paciente import Paciente
from src.modelo.medico import Medico
from src.modelo.especialidad import Especialidad
from src.modelo.turno import Turno
from src.modelo.receta import Receta
from src.modelo.historia_clinica import HistoriaClinica

class TestHistoriaClinica(unittest.TestCase):

    def setUp(self):
        self.paciente = Paciente("Ayrton Senna", "13131313", "24/03/1960")
        self.medico = Medico("Dr. Valtteri Bottas", "54545")
        self.pediatria = Especialidad("Pediatría", ["lunes", "miércoles"])
        self.medico.agregar_especialidad(self.pediatria)

        self.fecha_hora = datetime(2025, 6, 16, 10, 0)
        self.turno = Turno(self.paciente, self.medico, self.fecha_hora, "Pediatría")
        self.receta = Receta(self.paciente, self.medico, ["Aspirina 100mg"])

        self.historia = HistoriaClinica(self.paciente)

    def test_historia_clinica_nueva_sin_registros(self):
        self.assertEqual(len(self.historia.obtener_turnos()), 0)
        self.assertEqual(len(self.historia.obtener_recetas()), 0)
        self.assertIn("Ayrton Senna", str(self.historia))

    def test_agregar_y_obtener_turno(self):
        self.historia.agregar_turno(self.turno)
        turnos = self.historia.obtener_turnos()

        self.assertEqual(len(turnos), 1)
        self.assertEqual(turnos[0], self.turno)

    def test_agregar_y_obtener_receta(self):
        self.historia.agregar_receta(self.receta)
        recetas = self.historia.obtener_recetas()

        self.assertEqual(len(recetas), 1)
        self.assertEqual(recetas[0], self.receta)

    def test_turnos_y_recetas_son_listas_copiadas(self):
        self.historia.agregar_turno(self.turno)
        copia_turnos = self.historia.obtener_turnos()
        copia_turnos.clear()
        self.assertEqual(len(self.historia.obtener_turnos()), 1)

        self.historia.agregar_receta(self.receta)
        copia_recetas = self.historia.obtener_recetas()
        copia_recetas.clear()
        self.assertEqual(len(self.historia.obtener_recetas()), 1)

    def test_agregar_turno_none_lanza_error(self):
        with self.assertRaises(ValueError):
            self.historia.agregar_turno(None)

    def test_agregar_receta_none_lanza_error(self):
        with self.assertRaises(ValueError):
            self.historia.agregar_receta(None)

    def test_str_incluye_datos_de_historia_completa(self):
        self.historia.agregar_turno(self.turno)
        self.historia.agregar_receta(self.receta)
        texto = str(self.historia)

        self.assertIn("Ayrton Senna", texto)
        self.assertIn("Turnos", texto)
        self.assertIn("Recetas", texto)
        self.assertIn("Dr. Valtteri Bottas", texto)

    def test_orden_de_turnos_y_recetas(self):
        otro_turno = Turno(self.paciente, self.medico, datetime(2025, 8, 19, 11, 0), "Pediatría")
        otra_receta = Receta(self.paciente, self.medico, ["Ibuprofeno 200mg"])

        self.historia.agregar_turno(self.turno)
        self.historia.agregar_turno(otro_turno)

        self.historia.agregar_receta(self.receta)
        self.historia.agregar_receta(otra_receta)

        turnos = self.historia.obtener_turnos()
        recetas = self.historia.obtener_recetas()

        self.assertEqual(turnos[0], self.turno)
        self.assertEqual(turnos[1], otro_turno)
        self.assertEqual(recetas[0], self.receta)
        self.assertEqual(recetas[1], otra_receta)

    def test_historia_clinica_con_muchos_turnos_y_recetas(self):
        for i in range(10):
            nuevo_turno = Turno(self.paciente, self.medico, datetime(2025, 6, 16+i, 9, 0), "Pediatría")
            nueva_receta = Receta(self.paciente, self.medico, [f"Medicamento{i}"])
            self.historia.agregar_turno(nuevo_turno)
            self.historia.agregar_receta(nueva_receta)

        self.assertEqual(len(self.historia.obtener_turnos()), 10)
        self.assertEqual(len(self.historia.obtener_recetas()), 10)


if __name__ == "__main__":
    unittest.main()

from datetime import datetime
from ..modelo.paciente import Paciente
from ..modelo.medico import Medico
from ..modelo.especialidad import Especialidad
from ..modelo.clinica import Clinica
from ..modelo.excepciones import (
    PacienteNoEncontradoException,
    MedicoNoEncontradoException,
    MedicoNoDisponibleException,
    TurnoOcupadoException,
    RecetaInvalidaException
)

class CLI:
    def __init__(self):
        self.clinica = Clinica()

    def menu(self):
        print("\nInterfaz de la aplicacion")
        print("-" * 50)
        print("1 - Agregar paciente")
        print("2 - Agregar medico")
        print("3 - Agendar turno")
        print("4 - Agregar especialidad a medico")
        print("5 - Emitir receta")
        print("6 - Ver historia clinica")
        print("7 - Ver todos los turnos")
        print("8 - Ver todos los pacientes")
        print("9 - Ver todos los medicos")
        print("10 - Editar especialidad de medico")
        print("0 - Salir")
        print("-" * 50)

    def ejecutar(self):
        while True:
            self.menu()

            try:
                opcion = input("Selecciona una opcion: ").strip()

                if opcion == "0":
                    print("\nSaliendo de la aplicacion...")
                    break
                elif opcion == "1":
                    self.agregar_paciente()
                elif opcion == "2":
                    self.agregar_medico()
                elif opcion == "3":
                    self.agendar_turno()
                elif opcion == "4":
                    self.agregar_especialidad_a_medico()
                elif opcion == "5":
                    self.emitir_receta()
                elif opcion == "6":
                    self.ver_historia_clinica()
                elif opcion == "7":
                    self.ver_todos_los_turnos()
                elif opcion == "8":
                    self.ver_todos_los_pacientes()
                elif opcion == "9":
                    self.ver_todos_los_medicos()
                elif opcion == "10":
                    self.editar_especialidad_de_medico()
                else:
                    print("Opcion invalida. Seleccione de vuelta")
            except KeyboardInterrupt:
                print("Hasta luego")
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
                input("\nEnter para continuar")

    def agregar_paciente(self):
        print("\nAgregar paciente")
        print("-" * 50)
        while True:
            nombre = input("Ingrese el nombre del paciente: ").strip()
            if not nombre:
                print("El nombre no debe estar vacío. Inténtelo de nuevo.")
                continue 
            break
        while True:
            dni = input("Ingrese el DNI del paciente: ").strip()
            if not dni:
                print("El DNI no debe estar vacío. Inténtelo de nuevo.")
                continue 
            if not dni.isdigit():
                print("El DNI debe contener solo números. Inténtelo de nuevo.")
                continue 
            if len(dni) != 8:
                print("El DNI debe tener exactamente 8 dígitos. Inténtelo de nuevo.")
                continue
            break
        while True:
            fecha = input("Ingrese la fecha de nacimiento (dd/mm/aaaa): ").strip()
            if not fecha:
                print("La fecha de nacimiento no debe estar vacía. Inténtelo de nuevo.")
                continue  
            if not self._validar_fecha(fecha):
                print("La fecha debe estar en formato dd/mm/aaaa y ser válida. Inténtelo de nuevo.")
                continue
            if self._es_fecha_futura(fecha):
                print("La fecha de nacimiento no puede ser futura. Inténtelo de nuevo.")
                continue
            try:

                paciente = Paciente(nombre, dni, fecha)
                self.clinica.agregar_paciente(paciente)

                print("Paciente agregado")
                print(f"{paciente}")
                break
            except ValueError as e:
                print(f"Error en los datos: {e}")
                break
            except Exception as e:
                print(f"Error inesperado: {e}")
                break
            
        input("\nEnter para continuar")

    def agregar_medico(self):
        print("\nAgregar medico")
        print("-" * 50)

        try:
            while True:
                nombre = input("Nombre completo del medico: ").strip()
                if not nombre:
                    print("El nombre no debe estar vacío. Inténtelo de nuevo.")
                    continue 
                break
            while True:
                matricula = input("Matrícula: ").strip()
                if not matricula:
                    print("La matrícula no debe estar vacía. Inténtelo de nuevo.")
                    continue
                if not matricula.isdigit():
                    print("La matrícula debe contener solo números. Inténtelo de nuevo.")
                    continue
                if len(matricula) != 5:
                    print("La matrícula debe tener exactamente 5 dígitos. Inténtelo de nuevo.")
                    continue
                try:
                    self.clinica.validar_existencia_medico(matricula)
                    print(f"Ya existe un médico con la matrícula {matricula}. Ingrese una distinta.")
                    continue
                except MedicoNoEncontradoException:
                    break  # matrícula válida y no existente
                    
            

            medico = Medico(nombre, matricula)
            agrego_al_menos_una = False
            todos_los_dias = {"lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"}

            while True:
                # Revisar si quedan días libres
                dias_ocupados = set()
                for esp in medico._Medico__especialidades:
                    dias_ocupados.update(esp._Especialidad__dias)

                dias_disponibles = todos_los_dias - dias_ocupados
                if not dias_disponibles:
                    print("\nEl médico ya tiene todos los días ocupados. No se pueden agregar más especialidades.")
                    break

                especialidad_nombre = input("\nNombre de especialidad (Enter para terminar): ").strip()
                if not especialidad_nombre:
                    if not agrego_al_menos_una:
                        print("Debe ingresar al menos una especialidad.")
                        continue
                    else:
                        break
                if not especialidad_nombre:
                    if not agrego_al_menos_una:
                        print("Debe ingresar al menos una especialidad.")
                        continue
                    else:
                        break  # terminó de agregar
                # Solicitar días evitando conflictos
                while True:
                    dias = self.solicitar_dias_atencion(medico)
                    if not dias:
                        print("No se agregaron días válidos. Intente nuevamente.")
                        continue
                    try:
                        especialidad = Especialidad(especialidad_nombre, dias)
                        medico.agregar_especialidad(especialidad)
                        print(f"Especialidad '{especialidad_nombre}' agregada.")
                        agrego_al_menos_una = True
                        break  # sale del bucle de días y sigue con la siguiente especialidad
                    except ValueError as e:
                        print(f"Error: {e}")
                        print("Intentelo nuevamente con otros días.")
                        # vuelve a pedir los días
            self.clinica.agregar_medico(medico)
            print("Medico agregado")
            print(f"{medico}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")
    def solicitar_dias_atencion(self, medico):
        todos_los_dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
        
        dias_ocupados = set()
        for esp in medico._Medico__especialidades:
            dias_ocupados.update(esp._Especialidad__dias)

        dias_disponibles = [dia for dia in todos_los_dias if dia not in dias_ocupados]

        if not dias_disponibles:
            print("El médico no tiene más días disponibles.")
            return []

        print(f"Días disponibles: {', '.join(dias_disponibles)}")
        
        dias_input = input("Ingrese días de atención (separados por comas): ").strip()
        if not dias_input:
            return []

        dias = [d.strip().lower() for d in dias_input.split(",") if d.strip()]
        for d in dias:
            if d not in dias_disponibles:
                print(f"El día '{d}' ya está ocupado o no es válido. Intente de nuevo.")
                return self.solicitar_dias_atencion(medico)  # vuelve a pedir
        return dias
    
    def agendar_turno(self):
        print("\nAgendar turno")
        print("-" * 50)
        print("Escriba 'cancelar' o presione Enter vacío en cualquier momento para volver al menú.")

        try:
            while True:
                dni = input("DNI: ").strip()
                if not dni :
                    print("Agendamiento cancelado.")
                    return
                if not dni.isdigit() or len(dni) != 8:
                    print("DNI inválido. Debe tener 8 dígitos numéricos.")
                    continue
                try:
                    self.clinica.validar_existencia_paciente(dni)
                    break
                except PacienteNoEncontradoException as e:
                    print(f"{e}")
                    print("Por favor ingrese un DNI válido registrado en el sistema.")
            

            # Validar matrícula y especialidad
            while True:
                while True:
                    matricula = input("Matrícula médico: ").strip()
                    if not matricula :
                        print("Agendamiento cancelado.")
                        return
                    if not matricula.isdigit() or len(matricula) != 5:
                        print("Matrícula inválida. Debe tener 5 dígitos numéricos.")
                        continue
                    try:
                        self.clinica.validar_existencia_medico(matricula)
                        break
                    except MedicoNoEncontradoException as e:
                        print(f"{e}")
                        print("Por favor ingrese una matrícula válida registrada en el sistema.")
                if not matricula or matricula.lower() == "cancelar":
                    print("Agendamiento cancelado.")
                    return
                medico = self.clinica.obtener_medico_por_matricula(matricula)

                especialidades = medico._Medico__especialidades
                print("\nEspecialidades actuales:")
                for i, esp in enumerate(especialidades, 1):
                    print(f"{i}. {esp}")

                while True:
                    especialidad = input("Especialidad solicitada: ").strip().lower()

                    especialidades_nombres = [esp.obtener_especialidad().lower() for esp in especialidades]
                    if especialidad not in especialidades_nombres:
                        print(f"El médico no tiene la especialidad '{especialidad}'. Intente nuevamente.")
                        continue
                    break

                try:
                    self.clinica.validar_existencia_medico(matricula)
                    break
                except (MedicoNoEncontradoException, ValueError) as e:
                    print(f"Error: {e}")
                    print("Intente nuevamente con una matrícula y especialidad válidas.")
            
            # Validar fecha y hora
            while True:
                fecha_str = input("Fecha del turno (dd/mm/aaaa): ").strip()
                if not fecha_str or fecha_str.lower() == "cancelar":
                    print("Agendamiento cancelado.")
                    continue

                hora_str = input("Hora del turno (HH:MM): ").strip()
                if not hora_str or hora_str.lower() == "cancelar":
                    print("Agendamiento cancelado.")
                    continue

                try:
                    fecha_hora = self.parse_fecha_hora(fecha_str, hora_str)
                    break
                except ValueError as e:
                    print(f"Error en fecha u hora: {e}")
                    print("Por favor, ingrese una fecha y hora válidas.")



            # Agendar turno
            self.clinica.agendar_turno(dni, matricula, especialidad, fecha_hora)

            print("Turno agendado")
            print(f"Paciente DNI: {dni}")
            print(f"Médico: {matricula}")
            print(f"Fecha: {fecha_hora.strftime('%d/%m/%Y %H:%M')}")

        except (MedicoNoDisponibleException, TurnoOcupadoException) as e:
            print(f"{e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")

    def agregar_especialidad_a_medico(self):
        print("\nAgregar especialidad")
        print("-" * 50)

        try:
            matricula = input("Matricula del medico: ").strip()
            medico = self.clinica.obtener_medico_por_matricula(matricula)

            todos_los_dias = {"lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"}

            while True:
                # Revisar si quedan días libres
                dias_ocupados = set()
                for esp in medico._Medico__especialidades:
                    dias_ocupados.update(esp._Especialidad__dias)

                dias_disponibles = todos_los_dias - dias_ocupados
                if not dias_disponibles:
                    print("\nEl médico ya tiene todos los días ocupados. No se pueden agregar más especialidades.")
                    break
                medico = self.clinica.obtener_medico_por_matricula(matricula)

                especialidades = medico._Medico__especialidades
                print("\nEspecialidades actuales:")
                for i, esp in enumerate(especialidades, 1):
                    print(f"{i}. {esp}")

                especialidad_nombre = input("\nNombre de especialidad (Enter para terminar): ").strip()
                if not especialidad_nombre:
                    print("Operación cancelada o finalizada.")
                    break

                while True:
                    dias = self.solicitar_dias_atencion(medico)
                    if not dias:
                        print("No se agregaron días válidos. Intente nuevamente.")
                        continuar = input("¿Desea intentar de nuevo? (s/n): ").strip().lower()
                        if continuar != "s":
                            return
                        continue
                    try:
                        especialidad = Especialidad(especialidad_nombre, dias)
                        medico.agregar_especialidad(especialidad)
                        print(f"Especialidad '{especialidad_nombre}' agregada con éxito.")
                        break
                    except ValueError as e:
                        print(f"Error: {e}")
                        print("Intentelo nuevamente con otros días.")
            
        except MedicoNoEncontradoException as e:
            print(f"{e}")
        except ValueError as e:
            print(f"Error en los datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")

    def emitir_receta(self):
        print("\nEmitir receta")
        print("-" * 50)

        try:
            while True:
                dni = input("DNI: ").strip()
                if not dni or dni.lower() == "cancelar":
                    print("Receta cancelado.")
                    return
                if not dni.isdigit() or len(dni) != 8:
                    print("DNI inválido. Debe tener 8 dígitos numéricos.")
                    continue
                try:
                    self.clinica.validar_existencia_paciente(dni)
                    break
                except PacienteNoEncontradoException as e:
                    print(f"{e}")
                    print("Por favor ingrese un DNI válido registrado en el sistema.")
            
            while True:
                matricula = input("Matrícula médico: ").strip()
                if not matricula or matricula.lower() == "cancelar":
                    print("Receta cancelado.")
                    return
                if not matricula.isdigit() or len(matricula) != 5:
                    print("Matrícula inválida. Debe tener 5 dígitos numéricos.")
                    continue
                try:
                    self.clinica.validar_existencia_medico(matricula)
                    break
                except MedicoNoEncontradoException as e:
                    print(f"{e}")
                    print("Por favor ingrese una matrícula válida registrada en el sistema.")

            print("\nMedicamentos (Enter vacío para terminar): ")
            medicamentos = set()

            while True:
                medicamento = input("Medicamento: ").strip()
                if not medicamento:
                    if not medicamentos:
                        print("Debe ingresar al menos un medicamento.")
                        continue
                    break
                if medicamento.lower() in (m.lower() for m in medicamentos):
                    print("Este medicamento ya fue ingresado. No puede repetir.")
                    continue
                medicamentos.add(medicamento)
            
            self.clinica.emitir_receta(dni, matricula, medicamentos)

            print("Receta emitida")
            print(f"Paciente DNI: {dni}")
            print(f"Medico: {matricula}")
            print(f"Medicamentos: {', '.join(medicamentos)}")
        
        except (RecetaInvalidaException) as e:
            print(f"{e}")
        except ValueError as e:
            print(f"Error en los datos: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")

    def ver_historia_clinica(self):
        print("\n Ver historia clinica")
        print("-" * 50)

        try:
            dni = input("DNI paciente: ").strip()

            historia = self.clinica.obtener_historia_clinica(dni)

            print("\n" + "-" * 50)
            print(historia)
            print("-" * 50)

        except PacienteNoEncontradoException as e:
            print(f"{e}")
        except Exception as e:
            print(f"Error inesperado: {e}")
        
        input("\nEnter para continuar")

    def ver_todos_los_turnos(self):
        print("\nTodos los turnos")
        print("-" * 50)

        try:
            turnos = self.clinica.obtener_turnos()

            if not turnos:
                print("No hay turnos agendados")

            else:
                print(f"Total de turnos: {len(turnos)}")
                print("-" * 80)

            for i, turno in enumerate(turnos, 1):
                print(f"{i}. {turno}")

        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")

    def ver_todos_los_pacientes(self):
        print("\nTodos los pacientes")
        print("-" * 50)

        try:
            pacientes = self.clinica.obtener_pacientes()
            
            if not pacientes:
                print("No hay pacientes registrados")
            else:
                print(f"Total de pacientes: {len(pacientes)}")
                print("-" * 50)

                for i, paciente in enumerate(pacientes, 1):
                    print(f"{i}. {paciente}")

        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")
    
    def ver_todos_los_medicos(self):
        print("\nTodos los medicos")
        print("-" * 50)

        try:
            medicos = self.clinica.obtener_medicos()

            if not medicos:
                print("No hay medicos registrados")
            else:
                print(f"Total de medicos: {len(medicos)}")
                print(f"-" * 50)

                for i, medico in enumerate(medicos, 1):
                    print(f"{i}. {medico}")
     
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")

    def editar_especialidad_de_medico(self):
        print("\nEditar especialidad de un médico")
        print("-" * 50)

        try:
            while True:
                matricula = input("Matricula: ").strip()
                if not matricula:
                    print("El matricula no debe estar vacío. Inténtelo de nuevo.")
                    continue 
                if not matricula.isdigit():
                    print("El matricula debe contener solo números. Inténtelo de nuevo.")
                    continue 
                if len(matricula) != 5:
                    print("El matricula debe tener exactamente 5 dígitos. Inténtelo de nuevo.")
                    continue
                break
            medico = self.clinica.obtener_medico_por_matricula(matricula)

            especialidades = medico._Medico__especialidades

            print("\nEspecialidades actuales:")
            for i, esp in enumerate(especialidades, 1):
                print(f"{i}. {esp}")

            seleccion = input("Seleccione el número de la especialidad a editar: ").strip()
            if not seleccion.isdigit() or not (1 <= int(seleccion) <= len(especialidades)):
                print("Selección inválida.")
                return

            indice = int(seleccion) - 1
            especialidad_original = especialidades[indice]

            nuevo_nombre = input(f"Nuevo nombre (Enter para dejar como '{especialidad_original.obtener_especialidad()}'): ").strip()
            if not nuevo_nombre:
                nuevo_nombre = especialidad_original.obtener_especialidad()

            # Obtener días ocupados por las otras especialidades
            dias_ocupados = set()
            for i, esp in enumerate(especialidades):
                if i != indice:
                    dias_ocupados.update(esp._Especialidad__dias)

            # Mostrar días disponibles para evitar conflicto
            todos_los_dias = {"lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"}
            dias_disponibles = todos_los_dias - dias_ocupados
            if not dias_disponibles:
                print("No hay días disponibles para reasignar esta especialidad.")
                return

            print(f"Días disponibles: {', '.join(dias_disponibles)}")
            nuevos_dias_input = input("Nuevos días (separados por coma): ").strip()
            nuevos_dias = [d.strip().lower() for d in nuevos_dias_input.split(",") if d.strip()]

            # Validar que no se usen días ocupados
            for dia in nuevos_dias:
                if dia not in dias_disponibles:
                    print(f"El día '{dia}' ya está asignado a otra especialidad del médico.")
                    return

            # Reemplazar la especialidad
            from ..modelo.especialidad import Especialidad
            especialidad_actualizada = Especialidad(nuevo_nombre, nuevos_dias)
            especialidades[indice] = especialidad_actualizada

            print("\nEspecialidad actualizada correctamente.")
            print(especialidad_actualizada)

        except MedicoNoEncontradoException as e:
            print(f"{e}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

        input("\nEnter para continuar")


    def parse_fecha_hora(self, fecha_str, hora_str):
        try:
            fecha_hora_str = f"{fecha_str} {hora_str}"
            return datetime.strptime(fecha_hora_str, "%d/%m/%Y %H:%M")
        except ValueError:
            raise ValueError("Formato de fecha u hora invalido. (dd/mm/aaaa)")
    def _validar_fecha(self, fecha):
        try:
            datetime.strptime(fecha.strip(), "%d/%m/%Y")
            return True
        except ValueError:
            return False
    def _es_fecha_futura(self, fecha):
        try:
            fecha_obj = datetime.strptime(fecha.strip(), "%d/%m/%Y")
            return fecha_obj > datetime.now()
        except ValueError:
            return False

"""
Práctica Semana 2 — SIS206 POO II — UNAP Puno — 2026-II
ACTIVIDAD 2: Clase Docente — composición con Curso y propiedades calculadas.

Invariantes de clase:
  I1: dni tiene exactamente 8 dígitos
  I2: correo institucional termina en @unap.edu.pe
  I3: 0 <= len(cursos) <= _MAX_CURSOS (3)
  I4: fecha_nac es pasada y la edad resultante es >= 18
"""
import re
from datetime import date

from act1_curso import Curso


class Docente:
    _MAX_CURSOS = 3           # invariante: un docente no puede tener > 3 cursos
    _DOMINIO = "@unap.edu.pe"
    _PATRON_DNI = re.compile(r"^\d{8}$")

    def __init__(self, dni: str, nombres: str, apellidos: str,
                 correo: str, fecha_nac: date):
        self.__dni = self._validar_dni(dni)
        self.__nombres = self._validar_texto(nombres, "nombres")
        self.__apellidos = self._validar_texto(apellidos, "apellidos")
        self.__correo = self._validar_correo(correo)
        self.__fecha_nac = self._validar_fecha(fecha_nac)
        self.__cursos: list[Curso] = []

    # ------------------------------------------------------------------
    # Validadores (responsabilidad: verificar invariantes de entrada)
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_dni(dni: str) -> str:
        if not isinstance(dni, str) or not Docente._PATRON_DNI.match(dni.strip()):
            raise ValueError(f"DNI '{dni}' invalido: debe tener exactamente 8 digitos")
        return dni.strip()

    @staticmethod
    def _validar_correo(correo: str) -> str:
        if not isinstance(correo, str):
            raise ValueError("El correo debe ser una cadena de texto")
        correo = correo.strip().lower()
        if not correo.endswith(Docente._DOMINIO) or len(correo) <= len(Docente._DOMINIO):
            raise ValueError(
                f"Correo '{correo}' invalido: debe terminar en {Docente._DOMINIO}"
            )
        return correo

    @staticmethod
    def _validar_texto(valor: str, campo: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"El campo '{campo}' no puede estar vacio")
        return valor.strip()

    @staticmethod
    def _validar_fecha(fecha_nac: date) -> date:
        if not isinstance(fecha_nac, date):
            raise ValueError("fecha_nac debe ser un objeto datetime.date")
        if fecha_nac >= date.today():
            raise ValueError("La fecha de nacimiento debe ser anterior a hoy")
        return fecha_nac

    # ------------------------------------------------------------------
    # Getters de solo lectura (identidad: el DNI no se reescribe)
    # ------------------------------------------------------------------
    @property
    def dni(self) -> str:
        return self.__dni

    @property
    def nombres(self) -> str:
        return self.__nombres

    @property
    def apellidos(self) -> str:
        return self.__apellidos

    @property
    def fecha_nac(self) -> date:
        return self.__fecha_nac

    @property
    def cursos(self) -> tuple[Curso, ...]:
        """Devuelve una COPIA inmutable: impide que el cliente rompa el invariante I3."""
        return tuple(self.__cursos)

    # ------------------------------------------------------------------
    # correo : lectura / escritura validada
    # ------------------------------------------------------------------
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        self.__correo = self._validar_correo(valor)

    # ------------------------------------------------------------------
    # Propiedades CALCULADAS (derivadas del estado, nunca almacenadas)
    # ------------------------------------------------------------------
    @property
    def nombre_completo(self) -> str:
        return f"{self.__apellidos}, {self.__nombres}"

    @property
    def iniciales(self) -> str:
        return f"{self.__nombres[0]}.{self.__apellidos[0]}."

    @property
    def edad(self) -> int:
        """Calculada en tiempo real — no se almacena."""
        hoy = date.today()
        anios = hoy.year - self.__fecha_nac.year
        if (hoy.month, hoy.day) < (self.__fecha_nac.month, self.__fecha_nac.day):
            anios -= 1
        return anios

    @property
    def total_creditos(self) -> int:
        """Suma de creditos de todos los cursos asignados."""
        return sum(c.creditos for c in self.__cursos)

    @property
    def total_inscritos(self) -> int:
        """Total de estudiantes inscritos en todos sus cursos."""
        return sum(c.inscritos for c in self.__cursos)

    @property
    def carga_disponible(self) -> int:
        """Cursos que aun puede aceptar."""
        return self._MAX_CURSOS - len(self.__cursos)

    # ------------------------------------------------------------------
    # Lógica de negocio (verifica precondiciones)
    # ------------------------------------------------------------------
    def asignar_curso(self, curso: Curso) -> None:
        if not isinstance(curso, Curso):
            raise TypeError("Solo se pueden asignar objetos de tipo Curso")
        if len(self.__cursos) >= self._MAX_CURSOS:
            raise RuntimeError(
                f"{self.nombre_completo} ya tiene {self._MAX_CURSOS} cursos asignados"
            )
        if any(c.codigo == curso.codigo for c in self.__cursos):
            raise RuntimeError(f"El curso {curso.codigo} ya esta asignado")
        self.__cursos.append(curso)

    def __str__(self) -> str:
        return (f"Dr. {self.nombre_completo}"
                f" | Edad: {self.edad}"
                f" | Cursos: {len(self.__cursos)}"
                f" | Total creditos: {self.total_creditos}")


# --- Pruebas -----------------------------------------------------------
if __name__ == "__main__":
    print("=" * 62)
    print("ACTIVIDAD 2 — Docente: composicion y propiedades calculadas")
    print("=" * 62)

    doc = Docente("12345678", "Aldo Hernan", "Zanabria Galvez",
                  "azanabria@unap.edu.pe", date(1980, 5, 14))

    poo2 = Curso("SIS206", "POO II", 4, 30)
    poo2.inscribir_estudiante()
    poo2.inscribir_estudiante()
    doc.asignar_curso(poo2)

    print(doc)
    print(f"Total inscritos en sus cursos: {doc.total_inscritos}")
    print(f"Iniciales: {doc.iniciales} | Correo: {doc.correo}")

    print("\n-- Las propiedades calculadas siguen al estado real --------")
    bd = Curso("SIS301", "Base de Datos", 3, 25)
    for _ in range(5):
        bd.inscribir_estudiante()
    doc.asignar_curso(bd)
    print(f"  Tras asignar {bd.codigo}: creditos={doc.total_creditos}, "
          f"inscritos={doc.total_inscritos}, carga disponible={doc.carga_disponible}")
    poo2.inscribir_estudiante()
    print(f"  Tras 1 inscripcion mas en SIS206: inscritos={doc.total_inscritos} "
          f"(se recalcula, no se almacena)")

    print("\n-- Invariantes: validaciones del constructor ---------------")
    casos = [
        ("123", "A", "B", "a@unap.edu.pe", date(1980, 5, 14)),
        ("12345678", "A", "B", "a@gmail.com", date(1980, 5, 14)),
        ("12345678", "", "B", "a@unap.edu.pe", date(1980, 5, 14)),
        ("12345678", "A", "B", "a@unap.edu.pe", date(2090, 1, 1)),
    ]
    for caso in casos:
        try:
            Docente(*caso)
            print(f"  FALLO: {caso[0]}/{caso[3]} no lanzo excepcion")
        except ValueError as ex:
            print(f"  Error esperado: {ex}")

    print("\n-- Invariante: maximo 3 cursos -----------------------------")
    doc.asignar_curso(Curso("SIS404", "Ing. Software", 3, 20))
    try:
        doc.asignar_curso(Curso("SIS505", "Redes", 3, 20))
    except RuntimeError as ex:
        print(f"  RuntimeError esperado: {ex}")

    print("\n-- La lista interna esta protegida -------------------------")
    print(f"  type(doc.cursos) = {type(doc.cursos).__name__} (copia inmutable)")
    try:
        doc.cursos.append(Curso("SIS606", "IA", 3, 20))
    except AttributeError as ex:
        print(f"  AttributeError esperado: {ex}")
    print(f"  Cursos reales del docente: {len(doc.cursos)} (no se altero)")

    print("\n-- Propiedad calculada sin setter --------------------------")
    try:
        doc.nombre_completo = "otro"
    except AttributeError as ex:
        print(f"  AttributeError esperado: {ex}")

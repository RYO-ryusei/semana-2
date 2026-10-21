"""
Práctica Semana 2 — SIS206 POO II — UNAP Puno — 2026-II
ACTIVIDAD 1: Clase Curso con encapsulamiento estricto.

Invariantes de clase garantizados en todo momento:
  I1: codigo  cumple el patrón ^[A-Z]{2,4}\\d{3}$
  I2: 1 <= creditos <= 6
  I3: 1 <= cupos_maximo <= 50
  I4: 0 <= inscritos <= cupos_maximo
"""
import re


class Curso:
    _PATRON_CODIGO = re.compile(r"^[A-Z]{2,4}\d{3}$")
    _MIN_CREDITOS, _MAX_CREDITOS = 1, 6
    _MIN_CUPOS, _MAX_CUPOS = 1, 50

    def __init__(self, codigo: str, nombre: str, creditos: int, cupos_maximo: int):
        self.codigo = codigo                # usa setter (valida)
        self.nombre = nombre                # usa setter (valida)
        self.creditos = creditos            # usa setter (valida)
        self.cupos_maximo = cupos_maximo    # usa setter (valida)
        self.__inscritos = 0                # privado — sin setter público

    # ------------------------------------------------------------------
    # codigo : lectura / escritura validada
    # ------------------------------------------------------------------
    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("El codigo debe ser una cadena de texto")
        valor = valor.strip().upper()
        if not self._PATRON_CODIGO.match(valor):
            raise ValueError(
                f"Codigo '{valor}' invalido: se esperaba 2-4 letras mayusculas "
                f"seguidas de 3 digitos (ej. SIS206)"
            )
        self.__codigo = valor

    # ------------------------------------------------------------------
    # nombre : lectura / escritura validada (no vacío)
    # ------------------------------------------------------------------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del curso no puede estar vacio")
        self.__nombre = valor.strip()

    # ------------------------------------------------------------------
    # creditos : rango [1, 6]
    # ------------------------------------------------------------------
    @property
    def creditos(self) -> int:
        return self.__creditos

    @creditos.setter
    def creditos(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise ValueError("Los creditos deben ser un numero entero")
        if not (self._MIN_CREDITOS <= valor <= self._MAX_CREDITOS):
            raise ValueError(
                f"Creditos {valor} fuera de rango "
                f"[{self._MIN_CREDITOS},{self._MAX_CREDITOS}]"
            )
        self.__creditos = valor

    # ------------------------------------------------------------------
    # cupos_maximo : rango [1, 50] y nunca menor a los ya inscritos
    # ------------------------------------------------------------------
    @property
    def cupos_maximo(self) -> int:
        return self.__cupos_maximo

    @cupos_maximo.setter
    def cupos_maximo(self, valor: int) -> None:
        if not isinstance(valor, int) or isinstance(valor, bool):
            raise ValueError("Los cupos deben ser un numero entero")
        if not (self._MIN_CUPOS <= valor <= self._MAX_CUPOS):
            raise ValueError(
                f"Cupos {valor} fuera de rango "
                f"[{self._MIN_CUPOS},{self._MAX_CUPOS}]"
            )
        # Protege el invariante I4 al reducir el aforo de un curso en marcha
        inscritos = getattr(self, "_Curso__inscritos", 0)
        if valor < inscritos:
            raise ValueError(
                f"No se puede fijar cupos_maximo={valor}: ya hay {inscritos} inscritos"
            )
        self.__cupos_maximo = valor

    # ------------------------------------------------------------------
    # Propiedades de SOLO LECTURA / CALCULADAS
    # ------------------------------------------------------------------
    @property
    def inscritos(self) -> int:
        """Solo lectura — solo cambia por inscribir_estudiante()/retirar_estudiante()."""
        return self.__inscritos

    @property
    def cupos_disponibles(self) -> int:
        """Propiedad CALCULADA — sin setter."""
        return self.__cupos_maximo - self.__inscritos

    @property
    def esta_lleno(self) -> bool:
        """Propiedad calculada booleana."""
        return self.__inscritos >= self.__cupos_maximo

    @property
    def porcentaje_ocupacion(self) -> float:
        """Propiedad calculada: % de aforo usado, redondeado a 2 decimales."""
        return round(self.__inscritos / self.__cupos_maximo * 100, 2)

    # ------------------------------------------------------------------
    # Lógica de negocio (verifica precondiciones)
    # ------------------------------------------------------------------
    def inscribir_estudiante(self) -> None:
        """Controla el invariante: inscritos <= cupos_maximo."""
        if self.esta_lleno:
            raise RuntimeError(f"Curso {self.__codigo} sin cupos disponibles")
        self.__inscritos += 1

    def retirar_estudiante(self) -> None:
        """Precondición: debe existir al menos un inscrito (invariante inscritos >= 0)."""
        if self.__inscritos == 0:
            raise RuntimeError(f"Curso {self.__codigo} no tiene inscritos que retirar")
        self.__inscritos -= 1

    def __str__(self) -> str:
        return (f"{self.__codigo} - {self.__nombre}"
                f" ({self.__creditos} cr)"
                f" [{self.__inscritos}/{self.__cupos_maximo} inscritos]")

    def __repr__(self) -> str:
        return (f"Curso({self.__codigo!r}, {self.__nombre!r}, "
                f"{self.__creditos}, {self.__cupos_maximo})")


# --- Pruebas -----------------------------------------------------------
if __name__ == "__main__":
    print("=" * 62)
    print("ACTIVIDAD 1 — Clase Curso con encapsulamiento estricto")
    print("=" * 62)

    c = Curso("SIS206", "POO II", 4, 30)
    print(c)
    print(f"Cupos disponibles: {c.cupos_disponibles}")

    for _ in range(3):
        c.inscribir_estudiante()
    print(c)
    print(f"Ocupacion: {c.porcentaje_ocupacion}% | Lleno: {c.esta_lleno}")

    print("\n-- Invariantes: deben lanzar ValueError --------------------")
    for caso in [("X9", "nombre", 4, 30),
                 ("SIS206", "nombre", 0, 30),
                 ("SIS206", "nombre", 4, 0),
                 ("SIS206", "nombre", 7, 30),
                 ("sis206", "", 4, 30)]:
        try:
            Curso(*caso)
            print(f"  FALLO: {caso} no lanzo excepcion")
        except ValueError as ex:
            print(f"  Error esperado {caso}: {ex}")

    print("\n-- Propiedades calculadas: NO admiten asignacion -----------")
    for prop, val in [("cupos_disponibles", 99), ("esta_lleno", False), ("inscritos", 50)]:
        try:
            setattr(c, prop, val)
            print(f"  FALLO: se pudo asignar {prop}")
        except AttributeError as ex:
            print(f"  AttributeError esperado en '{prop}': {ex}")

    print("\n-- Invariante inscritos <= cupos_maximo --------------------")
    lleno = Curso("SIS101", "Algoritmica", 3, 2)
    lleno.inscribir_estudiante()
    lleno.inscribir_estudiante()
    try:
        lleno.inscribir_estudiante()
    except RuntimeError as ex:
        print(f"  RuntimeError esperado: {ex}")
    try:
        lleno.cupos_maximo = 1
    except ValueError as ex:
        print(f"  ValueError esperado al reducir aforo: {ex}")

    print("\n-- Name mangling ------------------------------------------")
    try:
        print(c.__codigo)
    except AttributeError as ex:
        print(f"  AttributeError esperado: {ex}")
    print(f"  Acceso 'forzado' (NO recomendado): {c._Curso__codigo}")

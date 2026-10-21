"""
Práctica Semana 2 — SIS206 POO II — UNAP Puno — 2026-II
ACTIVIDAD 5 — PROYECTO INTEGRADOR
Sistema de Gestión Académica — encapsulamiento estricto de las 3 clases propias:

  1) Calificacion  — nota ponderada de una evaluación
  2) Estudiante    — persona matriculable con avance curricular
  3) Matricula     — vínculo Estudiante ↔ Curso + sus calificaciones

Cada clase cumple el criterio de diseño exigido:
  · >= 3 atributos privados con invariante verificable
  · >= 1 propiedad calculada de solo lectura
  · >= 1 método de negocio que verifica una precondición
"""
import re
from datetime import date

from act1_curso import Curso


# =====================================================================
# CLASE 1 — Calificacion
# Responsabilidad única: representar UNA nota válida y ponderada.
# Invariantes:
#   I1: 0.0 <= valor <= 20.0
#   I2: 0.0 <  peso  <= 1.0
#   I3: tipo pertenece a TIPOS_VALIDOS
#   I4: recalificaciones <= MAX_RECALIFICACIONES
# =====================================================================
class Calificacion:
    _MIN_VALOR, _MAX_VALOR = 0.0, 20.0
    _NOTA_APROBATORIA = 11.0
    _TIPOS_VALIDOS = ("PRACTICA", "PARCIAL", "FINAL", "TRABAJO")
    _MAX_RECALIFICACIONES = 1

    def __init__(self, tipo: str, valor: float, peso: float):
        self.__tipo = None
        self.__valor = None
        self.__peso = None
        self.__recalificaciones = 0
        self.tipo = tipo        # usa setter
        self.valor = valor      # usa setter
        self.peso = peso        # usa setter

    # --- tipo -------------------------------------------------------
    @property
    def tipo(self) -> str:
        return self.__tipo

    @tipo.setter
    def tipo(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("El tipo de evaluacion debe ser texto")
        v = valor.strip().upper()
        if v not in self._TIPOS_VALIDOS:
            raise ValueError(
                f"Tipo '{valor}' invalido: use uno de {self._TIPOS_VALIDOS}"
            )
        self.__tipo = v

    # --- valor ------------------------------------------------------
    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, v: float) -> None:
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            raise ValueError("La calificacion debe ser numerica")
        if not (self._MIN_VALOR <= v <= self._MAX_VALOR):
            raise ValueError(
                f"Calificacion {v} fuera de rango "
                f"[{self._MIN_VALOR},{self._MAX_VALOR}]"
            )
        self.__valor = round(float(v), 2)

    # --- peso -------------------------------------------------------
    @property
    def peso(self) -> float:
        return self.__peso

    @peso.setter
    def peso(self, p: float) -> None:
        if isinstance(p, bool) or not isinstance(p, (int, float)):
            raise ValueError("El peso debe ser numerico")
        if not (0.0 < p <= 1.0):
            raise ValueError(f"Peso {p} fuera de rango (0.0, 1.0]")
        self.__peso = round(float(p), 4)

    # --- Propiedades CALCULADAS (solo lectura) -----------------------
    @property
    def puntos_ponderados(self) -> float:
        """Aporte real de esta nota al promedio final."""
        return round(self.__valor * self.__peso, 3)

    @property
    def esta_aprobada(self) -> bool:
        return self.__valor >= self._NOTA_APROBATORIA

    @property
    def literal(self) -> str:
        """Escala literal UNAP derivada del valor numerico."""
        v = self.__valor
        if v >= 18: return "AD (Logro destacado)"
        if v >= 14: return "A (Logro esperado)"
        if v >= 11: return "B (En proceso)"
        return "C (En inicio)"

    @property
    def recalificaciones(self) -> int:
        return self.__recalificaciones

    # --- Método de negocio con PRECONDICIÓN --------------------------
    def recalificar(self, nuevo_valor: float) -> None:
        """Precondición: no superar el máximo de recalificaciones permitidas."""
        if self.__recalificaciones >= self._MAX_RECALIFICACIONES:
            raise RuntimeError(
                f"La nota de {self.__tipo} ya fue recalificada "
                f"{self._MAX_RECALIFICACIONES} vez(ces): no admite otra revision"
            )
        self.valor = nuevo_valor        # reusa el setter -> invariante I1 intacto
        self.__recalificaciones += 1

    def __str__(self) -> str:
        return (f"{self.__tipo}: {self.__valor:.2f} "
                f"(peso {self.__peso:.0%}) -> {self.literal}")


# =====================================================================
# CLASE 2 — Estudiante
# Responsabilidad única: conocer la identidad y el avance curricular.
# Invariantes:
#   I1: codigo tiene exactamente 6 dígitos
#   I2: correo termina en @unap.edu.pe
#   I3: 1 <= semestre <= 10
#   I4: 0 <= creditos_aprobados <= TOTAL_CREDITOS_PLAN
# =====================================================================
class Estudiante:
    _PATRON_CODIGO = re.compile(r"^\d{6}$")
    _DOMINIO = "@unap.edu.pe"
    _MIN_SEMESTRE, _MAX_SEMESTRE = 1, 10
    TOTAL_CREDITOS_PLAN = 220

    def __init__(self, codigo: str, nombres: str, apellidos: str,
                 correo: str, semestre: int, creditos_aprobados: int = 0):
        self.__creditos_aprobados = 0
        self.codigo = codigo
        self.nombres = nombres
        self.apellidos = apellidos
        self.correo = correo
        self.semestre = semestre
        self.__creditos_aprobados = self._validar_creditos(creditos_aprobados)

    @classmethod
    def _validar_creditos(cls, c: int) -> int:
        if isinstance(c, bool) or not isinstance(c, int):
            raise ValueError("Los creditos aprobados deben ser un entero")
        if not (0 <= c <= cls.TOTAL_CREDITOS_PLAN):
            raise ValueError(
                f"Creditos aprobados {c} fuera de rango [0,{cls.TOTAL_CREDITOS_PLAN}]"
            )
        return c

    # --- codigo (identidad: setter validado) -------------------------
    @property
    def codigo(self) -> str:
        return self.__codigo

    @codigo.setter
    def codigo(self, valor: str) -> None:
        if not isinstance(valor, str) or not self._PATRON_CODIGO.match(valor.strip()):
            raise ValueError(f"Codigo '{valor}' invalido: debe tener 6 digitos")
        self.__codigo = valor.strip()

    # --- nombres / apellidos ----------------------------------------
    @property
    def nombres(self) -> str:
        return self.__nombres

    @nombres.setter
    def nombres(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Los nombres no pueden estar vacios")
        self.__nombres = valor.strip().title()

    @property
    def apellidos(self) -> str:
        return self.__apellidos

    @apellidos.setter
    def apellidos(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Los apellidos no pueden estar vacios")
        self.__apellidos = valor.strip().title()

    # --- correo ------------------------------------------------------
    @property
    def correo(self) -> str:
        return self.__correo

    @correo.setter
    def correo(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise ValueError("El correo debe ser texto")
        v = valor.strip().lower()
        if not v.endswith(self._DOMINIO) or len(v) <= len(self._DOMINIO):
            raise ValueError(f"Correo '{valor}' invalido: debe terminar en {self._DOMINIO}")
        self.__correo = v

    # --- semestre ----------------------------------------------------
    @property
    def semestre(self) -> int:
        return self.__semestre

    @semestre.setter
    def semestre(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("El semestre debe ser un entero")
        if not (self._MIN_SEMESTRE <= valor <= self._MAX_SEMESTRE):
            raise ValueError(
                f"Semestre {valor} fuera de rango "
                f"[{self._MIN_SEMESTRE},{self._MAX_SEMESTRE}]"
            )
        self.__semestre = valor

    # --- Propiedades CALCULADAS (solo lectura) -----------------------
    @property
    def creditos_aprobados(self) -> int:
        """Solo lectura: solo cambia mediante aprobar_creditos()."""
        return self.__creditos_aprobados

    @property
    def nombre_completo(self) -> str:
        return f"{self.__apellidos}, {self.__nombres}"

    @property
    def avance_curricular(self) -> float:
        """% del plan de estudios completado — derivado, nunca almacenado."""
        return round(self.__creditos_aprobados / self.TOTAL_CREDITOS_PLAN * 100, 2)

    @property
    def es_egresable(self) -> bool:
        return self.__creditos_aprobados >= self.TOTAL_CREDITOS_PLAN

    @property
    def condicion(self) -> str:
        """Regular / Observado según avance esperado para su semestre."""
        esperado = self.TOTAL_CREDITOS_PLAN / self._MAX_SEMESTRE * (self.__semestre - 1)
        return "REGULAR" if self.__creditos_aprobados >= esperado * 0.7 else "OBSERVADO"

    # --- Método de negocio con PRECONDICIÓN --------------------------
    def aprobar_creditos(self, cantidad: int) -> None:
        """Precondición: no exceder el total de créditos del plan de estudios."""
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValueError("La cantidad de creditos a aprobar debe ser un entero > 0")
        if self.__creditos_aprobados + cantidad > self.TOTAL_CREDITOS_PLAN:
            raise RuntimeError(
                f"{self.nombre_completo}: no puede superar los "
                f"{self.TOTAL_CREDITOS_PLAN} creditos del plan "
                f"(actual {self.__creditos_aprobados}, intento +{cantidad})"
            )
        self.__creditos_aprobados += cantidad

    def __str__(self) -> str:
        return (f"[{self.__codigo}] {self.nombre_completo} "
                f"| Sem. {self.__semestre} "
                f"| Avance: {self.avance_curricular}% "
                f"| {self.condicion}")


# =====================================================================
# CLASE 3 — Matricula
# Responsabilidad única: gestionar el vínculo Estudiante ↔ Curso
# y las calificaciones obtenidas en él.
# Invariantes:
#   I1: estado pertenece a ESTADOS_VALIDOS
#   I2: suma de pesos de las calificaciones <= 1.0
#   I3: len(calificaciones) <= MAX_EVALUACIONES
#   I4: fecha de matrícula no es futura
# =====================================================================
class Matricula:
    _ESTADOS_VALIDOS = ("ACTIVA", "RETIRADA", "CERRADA")
    _MAX_EVALUACIONES = 4
    _NOTA_APROBATORIA = 11.0

    def __init__(self, estudiante: Estudiante, curso: Curso,
                 fecha: date | None = None):
        if not isinstance(estudiante, Estudiante):
            raise TypeError("Se esperaba un objeto Estudiante")
        if not isinstance(curso, Curso):
            raise TypeError("Se esperaba un objeto Curso")
        fecha = fecha or date.today()
        if fecha > date.today():
            raise ValueError("La fecha de matricula no puede ser futura")

        self.__estudiante = estudiante
        self.__curso = curso
        self.__fecha = fecha
        self.__estado = "ACTIVA"
        self.__calificaciones: list[Calificacion] = []
        curso.inscribir_estudiante()     # el Curso protege su propio invariante

    # --- Getters de solo lectura -------------------------------------
    @property
    def estudiante(self) -> Estudiante:
        return self.__estudiante

    @property
    def curso(self) -> Curso:
        return self.__curso

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> str:
        return self.__estado

    @property
    def calificaciones(self) -> tuple[Calificacion, ...]:
        """Copia inmutable: el cliente no puede romper los invariantes I2/I3."""
        return tuple(self.__calificaciones)

    # --- Propiedades CALCULADAS (solo lectura) -----------------------
    @property
    def peso_acumulado(self) -> float:
        return round(sum(c.peso for c in self.__calificaciones), 4)

    @property
    def promedio(self) -> float:
        """Promedio ponderado sobre el peso efectivamente evaluado."""
        if not self.__calificaciones:
            return 0.0
        return round(
            sum(c.puntos_ponderados for c in self.__calificaciones) / self.peso_acumulado,
            2
        )

    @property
    def esta_completa(self) -> bool:
        return abs(self.peso_acumulado - 1.0) < 1e-9

    @property
    def esta_aprobada(self) -> bool:
        return self.esta_completa and self.promedio >= self._NOTA_APROBATORIA

    @property
    def resumen(self) -> str:
        return (f"{self.__estudiante.codigo} @ {self.__curso.codigo} "
                f"-> {self.promedio:.2f} ({self.__estado})")

    # --- Métodos de negocio con PRECONDICIÓN -------------------------
    def registrar_calificacion(self, calificacion: Calificacion) -> None:
        """Precondiciones: matrícula ACTIVA, cupo de evaluaciones y peso total <= 1.0."""
        if not isinstance(calificacion, Calificacion):
            raise TypeError("Se esperaba un objeto Calificacion")
        if self.__estado != "ACTIVA":
            raise RuntimeError(
                f"No se registran notas en una matricula {self.__estado}"
            )
        if len(self.__calificaciones) >= self._MAX_EVALUACIONES:
            raise RuntimeError(
                f"Se alcanzo el maximo de {self._MAX_EVALUACIONES} evaluaciones"
            )
        if self.peso_acumulado + calificacion.peso > 1.0 + 1e-9:
            raise RuntimeError(
                f"El peso total superaria 1.0 "
                f"(acumulado {self.peso_acumulado}, nuevo {calificacion.peso})"
            )
        self.__calificaciones.append(calificacion)

    def cerrar(self) -> None:
        """Precondición: el 100% del peso debe estar evaluado."""
        if self.__estado != "ACTIVA":
            raise RuntimeError(f"La matricula ya esta {self.__estado}")
        if not self.esta_completa:
            raise RuntimeError(
                f"No se puede cerrar: peso evaluado {self.peso_acumulado:.2f} de 1.00"
            )
        self.__estado = "CERRADA"
        if self.promedio >= self._NOTA_APROBATORIA:
            self.__estudiante.aprobar_creditos(self.__curso.creditos)

    def retirar(self) -> None:
        """Precondición: solo una matrícula ACTIVA puede retirarse."""
        if self.__estado != "ACTIVA":
            raise RuntimeError(f"La matricula ya esta {self.__estado}")
        self.__estado = "RETIRADA"
        self.__curso.retirar_estudiante()

    def __str__(self) -> str:
        return (f"Matricula {self.__fecha} | {self.__estudiante.nombre_completo} "
                f"| {self.__curso.codigo} | Estado: {self.__estado} "
                f"| Promedio: {self.promedio:.2f} "
                f"| Aprobada: {self.esta_aprobada}")


# --- Pruebas -----------------------------------------------------------
if __name__ == "__main__":
    print("=" * 66)
    print("ACTIVIDAD 5 — PROYECTO INTEGRADOR: Calificacion, Estudiante, Matricula")
    print("=" * 66)

    print("\n### CLASE 1 — Calificacion ###")
    n1 = Calificacion("PRACTICA", 15.5, 0.30)
    print(f"  {n1}")
    print(f"  Puntos ponderados: {n1.puntos_ponderados} | Aprobada: {n1.esta_aprobada}")
    for caso in [("EXAMEN_SORPRESA", 15, 0.3), ("FINAL", 21, 0.3), ("FINAL", 15, 1.5)]:
        try:
            Calificacion(*caso)
        except ValueError as ex:
            print(f"  ValueError esperado: {ex}")
    n1.recalificar(17.0)
    print(f"  Tras recalificar: {n1}")
    try:
        n1.recalificar(19.0)
    except RuntimeError as ex:
        print(f"  RuntimeError esperado: {ex}")

    print("\n### CLASE 2 — Estudiante ###")
    est = Estudiante("205678", "juan carlos", "mamani quispe",
                     "jmamani@unap.edu.pe", 5, 96)
    print(f"  {est}")
    print(f"  Egresable: {est.es_egresable} | Avance: {est.avance_curricular}%")
    for caso in [("2056", "A", "B", "a@unap.edu.pe", 5),
                 ("205678", "A", "B", "a@hotmail.com", 5),
                 ("205678", "A", "B", "a@unap.edu.pe", 12)]:
        try:
            Estudiante(*caso)
        except ValueError as ex:
            print(f"  ValueError esperado: {ex}")
    try:
        est.aprobar_creditos(200)
    except RuntimeError as ex:
        print(f"  RuntimeError esperado: {ex}")
    try:
        est.avance_curricular = 100
    except AttributeError as ex:
        print(f"  AttributeError esperado (calculada): {ex}")

    print("\n### CLASE 3 — Matricula ###")
    poo2 = Curso("SIS206", "POO II", 4, 30)
    mat = Matricula(est, poo2)
    print(f"  {mat}")
    print(f"  Inscritos en el curso tras matricular: {poo2.inscritos}")

    mat.registrar_calificacion(Calificacion("PRACTICA", 16, 0.30))
    mat.registrar_calificacion(Calificacion("PARCIAL", 13, 0.30))
    print(f"  Peso acumulado: {mat.peso_acumulado} | Promedio parcial: {mat.promedio}")
    try:
        mat.cerrar()
    except RuntimeError as ex:
        print(f"  RuntimeError esperado: {ex}")
    try:
        mat.registrar_calificacion(Calificacion("FINAL", 18, 0.60))
    except RuntimeError as ex:
        print(f"  RuntimeError esperado: {ex}")

    mat.registrar_calificacion(Calificacion("FINAL", 14, 0.40))
    print(f"  Peso completo: {mat.esta_completa} | Promedio final: {mat.promedio}")
    creditos_antes = est.creditos_aprobados
    mat.cerrar()
    print(f"  {mat}")
    print(f"  Creditos del estudiante: {creditos_antes} -> {est.creditos_aprobados}")
    try:
        mat.registrar_calificacion(Calificacion("TRABAJO", 20, 0.1))
    except RuntimeError as ex:
        print(f"  RuntimeError esperado: {ex}")
    try:
        mat.retirar()
    except RuntimeError as ex:
        print(f"  RuntimeError esperado: {ex}")

    print("\n### Retiro de una matricula ACTIVA ###")
    est2 = Estudiante("205679", "Maria", "Condori Apaza",
                      "mcondori@unap.edu.pe", 3, 40)
    mat2 = Matricula(est2, poo2)
    print(f"  Inscritos: {poo2.inscritos}")
    mat2.retirar()
    print(f"  Tras retirar -> estado={mat2.estado}, inscritos={poo2.inscritos}")

    print("\nOK: proyecto integrador validado.")

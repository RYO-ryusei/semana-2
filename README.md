# Práctica Semana 2 — SIS206 Programación Orientada a Objetos II

**Abstracción y Encapsulamiento Avanzado — Invariantes, Propiedades y Diseño por Responsabilidades**

Universidad Nacional del Altiplano · Escuela Profesional de Ingeniería de Sistemas
Semestre 2026-II · Docente: Dr. Aldo Hernán Zanabria Gálvez

---

## Contenido del repositorio

```
.
├── Practica_Semana2_SIS206.ipynb   # Notebook de Colab con las 5 actividades
├── src/
│   ├── python/
│   │   ├── act1_curso.py           # Actividad 1 — Curso con invariantes
│   │   ├── act2_docente.py         # Actividad 2 — Docente (composición + propiedades calculadas)
│   │   └── act5_proyecto.py        # Actividad 5 — Proyecto Integrador (Calificacion, Estudiante, Matricula)
│   └── cpp/
│       ├── Curso.hpp               # Actividad 3 — const correctness
│       ├── main.cpp                # Pruebas de Curso
│       ├── prueba_const.cpp        # Demuestra el error de compilación al violar const
│       ├── Calificacion.hpp        # Actividad 5 — equivalente C++17
│       ├── Estudiante.hpp
│       ├── Matricula.hpp
│       └── main_proyecto.cpp       # Pruebas del proyecto integrador en C++
├── docs/
│   ├── Informe_Semana2_SIS206.html # Informe completo (teoría, código, salidas, reflexión)
│   └── uml/
│       ├── uml_semana2.png         # Diagrama de clases (para el notebook / entrega)
│       └── uml_semana2.drawio      # Diagrama editable en app.diagrams.net
├── Makefile
└── .gitignore
```

## Cómo ejecutar

### Python (3.12+)

```bash
cd src/python
python3 act1_curso.py
python3 act2_docente.py
python3 act5_proyecto.py
```

### C++17

```bash
cd src/cpp
g++ -std=c++17 -Wall -Wextra -o prog main.cpp && ./prog
g++ -std=c++17 -Wall -Wextra -o proyecto main_proyecto.cpp && ./proyecto
```

O simplemente, desde la raíz del repo:

```bash
make run-python
make run-cpp
```

## Resumen de actividades

| # | Actividad | Archivo(s) |
|---|---|---|
| 1 | `@property` avanzado — invariantes con setters validados | `src/python/act1_curso.py` |
| 2 | Propiedades calculadas y composición | `src/python/act2_docente.py` |
| 3 | `const correctness` en C++17 | `src/cpp/Curso.hpp`, `main.cpp` |
| 4 | Tabla de equivalencias Python / C++ | ver `docs/Informe_Semana2_SIS206.html` |
| 5 | Proyecto Integrador (3 clases + UML) | `src/python/act5_proyecto.py`, `src/cpp/*.hpp`, `docs/uml/` |

El informe completo (`docs/Informe_Semana2_SIS206.html`) contiene el marco teórico, el código,
las salidas reales de ejecución/compilación, la tabla de equivalencias, el análisis de `const`,
el diagrama UML y las 4 preguntas de reflexión desarrolladas.

## Invariantes implementados

- **Curso**: código `^[A-Z]{2,4}\d{3}$`, `1 ≤ creditos ≤ 6`, `1 ≤ cupos_maximo ≤ 50`,
  `0 ≤ inscritos ≤ cupos_maximo`.
- **Docente**: DNI de 8 dígitos, correo `@unap.edu.pe`, máximo 3 cursos asignados.
- **Calificacion**: `0 ≤ valor ≤ 20`, `0 < peso ≤ 1`, tipo en un conjunto cerrado, máximo 1 recalificación.
- **Estudiante**: código de 6 dígitos, correo institucional, `1 ≤ semestre ≤ 10`, créditos dentro del plan (220).
- **Matricula**: estado en `{ACTIVA, RETIRADA, CERRADA}`, suma de pesos de notas `≤ 1.0`, máximo 4 evaluaciones.

## Commit sugerido

```bash
git add .
git commit -m "feat(semana2): encapsulamiento estricto e invariantes"
git push origin main
```

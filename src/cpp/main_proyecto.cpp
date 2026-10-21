// =====================================================================
// Proyecto Integrador - Semana 2 - Pruebas de las 3 clases en C++17
// Compilar: g++ -std=c++17 -Wall -Wextra -o proyecto main_proyecto.cpp
// =====================================================================
#include "Matricula.hpp"
#include <iostream>

int main() {
    std::cout << "======================================================\n";
    std::cout << "PROYECTO INTEGRADOR C++17 - Calificacion/Estudiante/Matricula\n";
    std::cout << "======================================================\n";

    std::cout << "\n### CLASE 1 - Calificacion ###\n";
    Calificacion n1("PRACTICA", 15.5, 0.30);
    n1.imprimir();
    std::cout << "  Puntos ponderados: " << n1.puntosPonderados() << "\n";
    try { Calificacion mala("SORPRESA", 15, 0.3); }
    catch (const std::invalid_argument& ex) { std::cout << "  " << ex.what() << "\n"; }
    try { Calificacion mala("FINAL", 21, 0.3); }
    catch (const std::invalid_argument& ex) { std::cout << "  " << ex.what() << "\n"; }
    n1.recalificar(17.0);
    std::cout << "  Tras recalificar: " << n1.getValor() << "\n";
    try { n1.recalificar(19.0); }
    catch (const std::runtime_error& ex) { std::cout << "  " << ex.what() << "\n"; }

    std::cout << "\n### CLASE 2 - Estudiante ###\n";
    Estudiante est("205678", "Juan Carlos", "Mamani Quispe",
                   "jmamani@unap.edu.pe", 5, 96);
    est.imprimir();
    try { Estudiante e("2056", "A", "B", "a@unap.edu.pe", 5); }
    catch (const std::invalid_argument& ex) { std::cout << "  " << ex.what() << "\n"; }
    try { Estudiante e("205678", "A", "B", "a@gmail.com", 5); }
    catch (const std::invalid_argument& ex) { std::cout << "  " << ex.what() << "\n"; }
    try { est.aprobarCreditos(200); }
    catch (const std::runtime_error& ex) { std::cout << "  " << ex.what() << "\n"; }

    std::cout << "\n### CLASE 3 - Matricula ###\n";
    Curso poo2("SIS206", "POO II", 4, 30);
    Matricula mat(est, poo2, "2026-09-17");
    mat.imprimir();
    std::cout << "  Inscritos en el curso: " << poo2.getInscritos() << "\n";

    mat.registrarCalificacion(Calificacion("PRACTICA", 16, 0.30));
    mat.registrarCalificacion(Calificacion("PARCIAL", 13, 0.30));
    std::cout << "  Peso acumulado: " << mat.pesoAcumulado()
              << " | Promedio parcial: " << mat.promedio() << "\n";
    try { mat.cerrar(); }
    catch (const std::runtime_error& ex) { std::cout << "  " << ex.what() << "\n"; }
    try { mat.registrarCalificacion(Calificacion("FINAL", 18, 0.60)); }
    catch (const std::runtime_error& ex) { std::cout << "  " << ex.what() << "\n"; }

    mat.registrarCalificacion(Calificacion("FINAL", 14, 0.40));
    int antes = est.getCreditosAprobados();
    mat.cerrar();
    mat.imprimir();
    std::cout << "  Creditos: " << antes << " -> " << est.getCreditosAprobados() << "\n";
    try { mat.retirar(); }
    catch (const std::runtime_error& ex) { std::cout << "  " << ex.what() << "\n"; }

    std::cout << "\n### Retiro de matricula ACTIVA ###\n";
    Estudiante est2("205679", "Maria", "Condori Apaza", "mcondori@unap.edu.pe", 3, 40);
    Matricula mat2(est2, poo2, "2026-09-17");
    std::cout << "  Inscritos: " << poo2.getInscritos() << "\n";
    mat2.retirar();
    std::cout << "  Tras retirar -> estado=" << mat2.getEstado()
              << ", inscritos=" << poo2.getInscritos() << "\n";

    std::cout << "\nOK: proyecto integrador C++ validado.\n";
    return 0;
}

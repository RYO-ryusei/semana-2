// =====================================================================
// Practica Semana 2 - Actividad 3: main.cpp - pruebas de Curso
// Compilar: g++ -std=c++17 -Wall -Wextra -o prog main.cpp
// =====================================================================
#include "Curso.hpp"
#include <iostream>

// Demuestra el beneficio de const correctness: esta funcion recibe una
// referencia constante y SOLO puede invocar metodos marcados const.
void reportar(const Curso& c) {
    std::cout << "  [reporte] " << c.getCodigo()
              << " ocupacion=" << c.porcentajeOcupacion() << "%"
              << " disponibles=" << c.cuposDisponibles()
              << " lleno=" << std::boolalpha << c.estaLleno() << "\n";
    // c.inscribirEstudiante();  // ERROR de compilacion: metodo no-const
}

int main() {
    std::cout << "==============================================\n";
    std::cout << "ACTIVIDAD 3 - Curso en C++17 (const correctness)\n";
    std::cout << "==============================================\n";

    Curso c("SIS206", "POO II", 4, 30);
    c.inscribirEstudiante();
    c.inscribirEstudiante();
    c.inscribirEstudiante();
    c.imprimir();
    reportar(c);

    std::cout << "\n-- Setters validados: std::invalid_argument --\n";
    try { Curso bad("SIS206", "bad", 0, 30); }
    catch (const std::invalid_argument& ex) { std::cout << "  " << ex.what() << "\n"; }

    try { Curso bad("X9", "bad", 4, 30); }
    catch (const std::invalid_argument& ex) { std::cout << "  " << ex.what() << "\n"; }

    try { Curso bad("SIS206", "bad", 4, 99); }
    catch (const std::invalid_argument& ex) { std::cout << "  " << ex.what() << "\n"; }

    try { c.setCuposMaximo(2); }
    catch (const std::invalid_argument& ex) { std::cout << "  " << ex.what() << "\n"; }

    std::cout << "\n-- Invariante inscritos <= cuposMaximo --\n";
    Curso lleno("SIS101", "Algoritmica", 3, 2);
    lleno.inscribirEstudiante();
    lleno.inscribirEstudiante();
    try { lleno.inscribirEstudiante(); }
    catch (const std::runtime_error& ex) { std::cout << "  " << ex.what() << "\n"; }

    std::cout << "\n-- Un objeto const solo admite metodos const --\n";
    const Curso fijo("SIS301", "Base de Datos", 3, 25);
    fijo.imprimir();
    reportar(fijo);
    // fijo.inscribirEstudiante();  // ERROR: descarta el calificador const
    // fijo.setCreditos(5);         // ERROR: descarta el calificador const

    std::cout << "\nOK: todas las pruebas ejecutadas.\n";
    return 0;
}

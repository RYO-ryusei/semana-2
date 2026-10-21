// =====================================================================
// Practica Semana 2 - SIS206 POO II - UNAP Puno - 2026-II
// ACTIVIDAD 3: Curso.hpp - encapsulamiento C++17, const correctness
// Invariantes: codigo ~ [A-Z]{2,4}[0-9]{3} | 1<=creditos<=6
//              1<=cuposMaximo<=50 | 0<=inscritos<=cuposMaximo
// =====================================================================
#pragma once

#include <string>
#include <regex>
#include <stdexcept>
#include <iostream>
#include <utility>

class Curso {
    std::string codigo_;
    std::string nombre_;
    int creditos_ = 0;
    int cuposMaximo_ = 0;
    int inscritos_ = 0;              // inicializado en declaracion

    static const std::regex& patronCodigo() {
        static const std::regex patron(R"(^[A-Z]{2,4}[0-9]{3}$)");
        return patron;
    }

public:
    static constexpr int MIN_CREDITOS = 1;
    static constexpr int MAX_CREDITOS = 6;
    static constexpr int MIN_CUPOS    = 1;
    static constexpr int MAX_CUPOS    = 50;

    Curso(std::string codigo, std::string nombre, int creditos, int cuposMaximo) {
        setCodigo(codigo);           // validar en el constructor
        setNombre(std::move(nombre));
        setCreditos(creditos);
        setCuposMaximo(cuposMaximo);
    }

    // --- Setters validados -------------------------------------------
    void setCodigo(const std::string& cod) {
        if (!std::regex_match(cod, patronCodigo()))
            throw std::invalid_argument("Codigo invalido: '" + cod +
                                        "' (se espera 2-4 letras mayusculas + 3 digitos)");
        codigo_ = cod;
    }

    void setNombre(std::string nom) {
        if (nom.empty())
            throw std::invalid_argument("El nombre del curso no puede estar vacio");
        nombre_ = std::move(nom);
    }

    void setCreditos(int c) {
        if (c < MIN_CREDITOS || c > MAX_CREDITOS)
            throw std::invalid_argument("Creditos fuera de rango [1,6]");
        creditos_ = c;
    }

    void setCuposMaximo(int q) {
        if (q < MIN_CUPOS || q > MAX_CUPOS)
            throw std::invalid_argument("Cupos fuera de rango [1,50]");
        if (q < inscritos_)          // protege el invariante inscritos_ <= cuposMaximo_
            throw std::invalid_argument("Cupos menores a los estudiantes ya inscritos");
        cuposMaximo_ = q;
    }

    // --- Getters (const - no modifican el objeto) ---------------------
    const std::string& getCodigo() const { return codigo_; }
    const std::string& getNombre() const { return nombre_; }
    int getCreditos()    const { return creditos_; }
    int getCuposMaximo() const { return cuposMaximo_; }
    int getInscritos()   const { return inscritos_; }

    // --- Propiedades calculadas (const) ------------------------------
    int  cuposDisponibles() const { return cuposMaximo_ - inscritos_; }
    bool estaLleno()        const { return inscritos_ >= cuposMaximo_; }
    double porcentajeOcupacion() const {
        return 100.0 * inscritos_ / cuposMaximo_;
    }

    // --- Logica de negocio (NO const: modifica el estado) ------------
    void inscribirEstudiante() {
        if (estaLleno())
            throw std::runtime_error("Curso sin cupos: " + codigo_);
        ++inscritos_;
    }

    void retirarEstudiante() {
        if (inscritos_ == 0)
            throw std::runtime_error("Curso sin inscritos: " + codigo_);
        --inscritos_;
    }

    void imprimir() const {
        std::cout << codigo_ << " - " << nombre_
                  << " (" << creditos_ << " cr)"
                  << " [" << inscritos_ << "/" << cuposMaximo_ << "]\n";
    }
};

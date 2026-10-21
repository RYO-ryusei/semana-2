// =====================================================================
// Proyecto Integrador - Semana 2 - Clase 2: Estudiante
// Invariantes: codigo_ = 6 digitos | correo_ termina en @unap.edu.pe
//              1<=semestre_<=10 | 0<=creditosAprobados_<=TOTAL_CREDITOS_PLAN
// =====================================================================
#pragma once

#include <string>
#include <regex>
#include <stdexcept>
#include <iostream>
#include <iomanip>

class Estudiante {
    std::string codigo_;
    std::string nombres_;
    std::string apellidos_;
    std::string correo_;
    int semestre_ = 1;
    int creditosAprobados_ = 0;

    static const std::regex& patronCodigo() {
        static const std::regex p(R"(^[0-9]{6}$)");
        return p;
    }

public:
    static constexpr int TOTAL_CREDITOS_PLAN = 220;
    static constexpr int MIN_SEMESTRE = 1;
    static constexpr int MAX_SEMESTRE = 10;

    Estudiante(const std::string& codigo, const std::string& nombres,
               const std::string& apellidos, const std::string& correo,
               int semestre, int creditosAprobados = 0) {
        setCodigo(codigo);
        setNombres(nombres);
        setApellidos(apellidos);
        setCorreo(correo);
        setSemestre(semestre);
        setCreditosAprobados(creditosAprobados);
    }

    // --- Setters validados -------------------------------------------
    void setCodigo(const std::string& c) {
        if (!std::regex_match(c, patronCodigo()))
            throw std::invalid_argument("Codigo invalido: debe tener 6 digitos");
        codigo_ = c;
    }

    void setNombres(const std::string& n) {
        if (n.empty()) throw std::invalid_argument("Los nombres no pueden estar vacios");
        nombres_ = n;
    }

    void setApellidos(const std::string& a) {
        if (a.empty()) throw std::invalid_argument("Los apellidos no pueden estar vacios");
        apellidos_ = a;
    }

    void setCorreo(const std::string& c) {
        const std::string dominio = "@unap.edu.pe";
        if (c.size() <= dominio.size() ||
            c.compare(c.size() - dominio.size(), dominio.size(), dominio) != 0)
            throw std::invalid_argument("Correo invalido: debe terminar en @unap.edu.pe");
        correo_ = c;
    }

    void setSemestre(int s) {
        if (s < MIN_SEMESTRE || s > MAX_SEMESTRE)
            throw std::invalid_argument("Semestre fuera de rango [1,10]");
        semestre_ = s;
    }

    void setCreditosAprobados(int c) {
        if (c < 0 || c > TOTAL_CREDITOS_PLAN)
            throw std::invalid_argument("Creditos aprobados fuera de rango [0,220]");
        creditosAprobados_ = c;
    }

    // --- Getters const -----------------------------------------------
    const std::string& getCodigo()    const { return codigo_; }
    const std::string& getNombres()   const { return nombres_; }
    const std::string& getApellidos() const { return apellidos_; }
    const std::string& getCorreo()    const { return correo_; }
    int getSemestre() const { return semestre_; }
    int getCreditosAprobados() const { return creditosAprobados_; }

    // --- Propiedades calculadas (const) ------------------------------
    std::string nombreCompleto() const { return apellidos_ + ", " + nombres_; }
    double avanceCurricular() const {
        return 100.0 * creditosAprobados_ / TOTAL_CREDITOS_PLAN;
    }
    bool esEgresable() const { return creditosAprobados_ >= TOTAL_CREDITOS_PLAN; }
    std::string condicion() const {
        double esperado = static_cast<double>(TOTAL_CREDITOS_PLAN) / MAX_SEMESTRE
                          * (semestre_ - 1);
        return (creditosAprobados_ >= esperado * 0.7) ? "REGULAR" : "OBSERVADO";
    }

    // --- Negocio con precondicion ------------------------------------
    void aprobarCreditos(int cantidad) {
        if (cantidad <= 0)
            throw std::invalid_argument("La cantidad de creditos debe ser > 0");
        if (creditosAprobados_ + cantidad > TOTAL_CREDITOS_PLAN)
            throw std::runtime_error(nombreCompleto() +
                ": no puede superar los 220 creditos del plan");
        creditosAprobados_ += cantidad;
    }

    void imprimir() const {
        std::cout << "[" << codigo_ << "] " << nombreCompleto()
                  << " | Sem. " << semestre_
                  << " | Avance: " << std::fixed << std::setprecision(2)
                  << avanceCurricular() << "%"
                  << " | " << condicion() << "\n";
    }
};

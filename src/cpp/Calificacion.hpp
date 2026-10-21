// =====================================================================
// Proyecto Integrador - Semana 2 - Clase 1: Calificacion
// Invariantes: 0<=valor_<=20 | 0<peso_<=1 | tipo_ valido
//              recalificaciones_ <= MAX_RECALIFICACIONES
// =====================================================================
#pragma once

#include <string>
#include <array>
#include <algorithm>
#include <stdexcept>
#include <iostream>
#include <iomanip>

class Calificacion {
    std::string tipo_;
    double valor_ = 0.0;
    double peso_ = 0.0;
    int recalificaciones_ = 0;

public:
    static constexpr double MIN_VALOR = 0.0;
    static constexpr double MAX_VALOR = 20.0;
    static constexpr double NOTA_APROBATORIA = 11.0;
    static constexpr int MAX_RECALIFICACIONES = 1;

    Calificacion(const std::string& tipo, double valor, double peso) {
        setTipo(tipo);
        setValor(valor);
        setPeso(peso);
    }

    // --- Setters validados -------------------------------------------
    void setTipo(const std::string& t) {
        static const std::array<std::string, 4> validos =
            {"PRACTICA", "PARCIAL", "FINAL", "TRABAJO"};
        std::string up = t;
        std::transform(up.begin(), up.end(), up.begin(),
                       [](unsigned char ch) { return static_cast<char>(std::toupper(ch)); });
        if (std::find(validos.begin(), validos.end(), up) == validos.end())
            throw std::invalid_argument("Tipo de evaluacion invalido: " + t);
        tipo_ = up;
    }

    void setValor(double v) {
        if (v < MIN_VALOR || v > MAX_VALOR)
            throw std::invalid_argument("Calificacion fuera de rango [0,20]");
        valor_ = v;
    }

    void setPeso(double p) {
        if (p <= 0.0 || p > 1.0)
            throw std::invalid_argument("Peso fuera de rango (0,1]");
        peso_ = p;
    }

    // --- Getters const -----------------------------------------------
    const std::string& getTipo() const { return tipo_; }
    double getValor() const { return valor_; }
    double getPeso()  const { return peso_; }
    int getRecalificaciones() const { return recalificaciones_; }

    // --- Propiedades calculadas (const) ------------------------------
    double puntosPonderados() const { return valor_ * peso_; }
    bool estaAprobada() const { return valor_ >= NOTA_APROBATORIA; }
    std::string literal() const {
        if (valor_ >= 18) return "AD (Logro destacado)";
        if (valor_ >= 14) return "A (Logro esperado)";
        if (valor_ >= 11) return "B (En proceso)";
        return "C (En inicio)";
    }

    // --- Negocio con precondicion ------------------------------------
    void recalificar(double nuevoValor) {
        if (recalificaciones_ >= MAX_RECALIFICACIONES)
            throw std::runtime_error("La nota de " + tipo_ + " ya fue recalificada");
        setValor(nuevoValor);       // reusa el setter: invariante intacto
        ++recalificaciones_;
    }

    void imprimir() const {
        std::cout << tipo_ << ": " << std::fixed << std::setprecision(2) << valor_
                  << " (peso " << peso_ << ") -> " << literal() << "\n";
    }
};

// =====================================================================
// Proyecto Integrador - Semana 2 - Clase 3: Matricula
// Invariantes: estado_ valido | suma de pesos <= 1.0
//              calificaciones_.size() <= MAX_EVALUACIONES
// Nota: usa asociacion por referencia a Estudiante y Curso (no los posee).
// =====================================================================
#pragma once

#include "Curso.hpp"
#include "Estudiante.hpp"
#include "Calificacion.hpp"

#include <vector>
#include <string>
#include <stdexcept>
#include <numeric>
#include <cmath>
#include <iostream>
#include <iomanip>

class Matricula {
    Estudiante* estudiante_;            // asociacion: no gestiona su ciclo de vida
    Curso* curso_;
    std::string fecha_;
    std::string estado_ = "ACTIVA";
    std::vector<Calificacion> calificaciones_;

public:
    static constexpr std::size_t MAX_EVALUACIONES = 4;
    static constexpr double NOTA_APROBATORIA = 11.0;

    Matricula(Estudiante& estudiante, Curso& curso, std::string fecha)
        : estudiante_(&estudiante), curso_(&curso), fecha_(std::move(fecha)) {
        if (fecha_.empty())
            throw std::invalid_argument("La fecha de matricula no puede estar vacia");
        curso_->inscribirEstudiante();  // el Curso protege su propio invariante
    }

    // --- Getters const -----------------------------------------------
    const Estudiante& getEstudiante() const { return *estudiante_; }
    const Curso& getCurso() const { return *curso_; }
    const std::string& getFecha()  const { return fecha_; }
    const std::string& getEstado() const { return estado_; }
    const std::vector<Calificacion>& getCalificaciones() const { return calificaciones_; }

    // --- Propiedades calculadas (const) ------------------------------
    double pesoAcumulado() const {
        double s = 0.0;
        for (const auto& c : calificaciones_) s += c.getPeso();
        return s;
    }

    double promedio() const {
        if (calificaciones_.empty()) return 0.0;
        double puntos = 0.0;
        for (const auto& c : calificaciones_) puntos += c.puntosPonderados();
        return puntos / pesoAcumulado();
    }

    bool estaCompleta() const { return std::fabs(pesoAcumulado() - 1.0) < 1e-9; }
    bool estaAprobada() const { return estaCompleta() && promedio() >= NOTA_APROBATORIA; }

    // --- Negocio con precondiciones ----------------------------------
    void registrarCalificacion(const Calificacion& cal) {
        if (estado_ != "ACTIVA")
            throw std::runtime_error("No se registran notas en una matricula " + estado_);
        if (calificaciones_.size() >= MAX_EVALUACIONES)
            throw std::runtime_error("Se alcanzo el maximo de evaluaciones");
        if (pesoAcumulado() + cal.getPeso() > 1.0 + 1e-9)
            throw std::runtime_error("El peso total superaria 1.0");
        calificaciones_.push_back(cal);
    }

    void cerrar() {
        if (estado_ != "ACTIVA")
            throw std::runtime_error("La matricula ya esta " + estado_);
        if (!estaCompleta())
            throw std::runtime_error("No se puede cerrar: falta evaluar peso");
        estado_ = "CERRADA";
        if (promedio() >= NOTA_APROBATORIA)
            estudiante_->aprobarCreditos(curso_->getCreditos());
    }

    void retirar() {
        if (estado_ != "ACTIVA")
            throw std::runtime_error("La matricula ya esta " + estado_);
        estado_ = "RETIRADA";
        curso_->retirarEstudiante();
    }

    void imprimir() const {
        std::cout << "Matricula " << fecha_ << " | " << estudiante_->nombreCompleto()
                  << " | " << curso_->getCodigo()
                  << " | Estado: " << estado_
                  << " | Promedio: " << std::fixed << std::setprecision(2) << promedio()
                  << " | Aprobada: " << std::boolalpha << estaAprobada() << "\n";
    }
};

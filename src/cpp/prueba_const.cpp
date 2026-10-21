#include "Curso.hpp"
void reportar(const Curso& c) { c.imprimir(); c.inscribirEstudiante(); }
int main() { const Curso f("SIS206","POO II",4,30); f.setCreditos(5); reportar(f); }

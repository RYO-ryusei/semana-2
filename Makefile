.PHONY: run-python run-cpp clean

run-python:
	cd src/python && python3 act1_curso.py
	cd src/python && python3 act2_docente.py
	cd src/python && python3 act5_proyecto.py

run-cpp:
	cd src/cpp && g++ -std=c++17 -Wall -Wextra -o prog main.cpp && ./prog
	cd src/cpp && g++ -std=c++17 -Wall -Wextra -o proyecto main_proyecto.cpp && ./proyecto

clean:
	rm -f src/cpp/prog src/cpp/proyecto
	find . -name "__pycache__" -type d -exec rm -rf {} +

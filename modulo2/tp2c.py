import numpy as np
import matplotlib.pyplot as plt

# 1. Parámetros previos
gamma = 0.45041653
a = 3.0
h = 2.5

# Definimos la función de la catenaria
def catenaria(x):
    return (1 / gamma) * (np.cosh(gamma * x) - np.cosh(gamma * a)) + h

# 2. Generar los 8 puntos igualmente espaciados
x_puntos = np.linspace(-a, a, 8)
y_puntos = catenaria(x_puntos)

# 3. Armar el sistema de Cuadrados Mínimos (Ecuaciones Normales)
# Matriz de Vandermonde de tamaño 8x5
A = np.column_stack([x_puntos**0, x_puntos**1, x_puntos**2, x_puntos**3, x_puntos**4])

# Matriz AtA (5x5) y vector Aty (5x1)
AtA = A.T @ A
Aty = A.T @ y_puntos

# Resolver el sistema de ecuaciones lineales matricial
# (Esto internamente usa rutinas de álgebra lineal para despejar 'c')
coeficientes = np.linalg.solve(AtA, Aty)
c0, c1, c2, c3, c4 = coeficientes

print("Coeficientes del polinomio P4(x):")
print(f"c0 (independiente) = {c0: .6f}")
print(f"c1 (lineal)        = {c1: .6f}")
print(f"c2 (cuadrático)    = {c2: .6f}")
print(f"c3 (cúbico)        = {c3: .6f}")
print(f"c4 (cuártico)      = {c4: .6f}")

# 4. Cálculo del error en el punto más bajo (x = 0)
y_min_real = catenaria(0)
y_min_aprox = c0  # P4(0) = c0

error_minimo = abs(y_min_real - y_min_aprox)

print(f"\nAltura mínima real de la soga: {y_min_real:.6f} m")
print(f"Altura mínima aproximada P4(0): {y_min_aprox:.6f} m")
print(f"Error absoluto en la aproximación: {error_minimo:.6e} m")

# 5. Gráfica Comparativa
x_continuo = np.linspace(-a, a, 200)
y_continuo = catenaria(x_continuo)
# Evaluamos el polinomio para la gráfica usando los coeficientes
y_polinomio = c0 + c1*x_continuo + c2*(x_continuo**2) + c3*(x_continuo**3) + c4*(x_continuo**4)

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x_continuo, y_continuo, 'b-', linewidth=2, label='Catenaria real', alpha=0.7)
ax.plot(x_continuo, y_polinomio, 'r--', linewidth=2, label='Ajuste P4(x)', alpha=0.9)
ax.plot(x_puntos, y_puntos, 'ko', markersize=6, label='8 puntos de ajuste')

# Marcamos el error en el centro
ax.plot(0, y_min_real, 'bx', markersize=10, label='Mínimo real')
ax.plot(0, y_min_aprox, 'rx', markersize=10, label='Mínimo aprox.')

ax.set_title('Ajuste por Cuadrados Mínimos (Grado 4)', fontsize=14)
ax.set_xlabel('Posición $x$ [m]')
ax.set_ylabel('Altura $y$ [m]')
ax.grid(True, linestyle=':')
ax.legend()
plt.savefig('tp2c.png', dpi=300)
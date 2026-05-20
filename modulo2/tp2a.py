import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve

# 1. Parámetros dados
L = 8.0
a = 3.0
h = 2.5

# Definición de la función y su derivada
def f(gamma):
    return np.sinh(3 * gamma) - 4 * gamma

def df(gamma):
    return 3 * np.cosh(3 * gamma) - 4

# Implementación del Método de Newton-Raphson
def newton_raphson(func, dfunc, x0, tol=1e-6, max_iter=20):
    """
    func: Función f(x)
    dfunc: Derivada f'(x)
    x0: Valor inicial (guess)
    tol: Tolerancia para el criterio de parada
    max_iter: Número máximo de iteraciones permitidas
    """
    x_n = x0
    print(f"{'Iteración':<10} | {'gamma_n':<15} | {'f(gamma_n)':<15}")
    print("-" * 45)
    
    for n in range(max_iter):
        f_val = func(x_n)
        
        # Criterio de parada: si la función está muy cerca de 0
        if abs(f_val) < tol:
            print("-" * 45)
            print(f"Convergencia alcanzada en {n} iteraciones.")
            return x_n
        
        df_val = dfunc(x_n)
        
        # Evitar división por cero si la derivada se anula
        if df_val == 0:
            print("Error: La derivada es cero. El método falla.")
            return None
            
        print(f"{n:<10} | {x_n:<15.8f} | {f_val:<15.8e}")
        
        # Fórmula de iteración de Newton
        x_n = x_n - f_val / df_val
        
    print("Se alcanzó el número máximo de iteraciones sin converger.")
    return x_n

# --- EJECUCIÓN DEL PROBLEMA ---

# Usamos el mismo valor inicial que le dimos a scipy
gamma_inicial = 0.5 
gamma_calculado = newton_raphson(f, df, gamma_inicial)

print(f"\nValor final de gamma calculado: {gamma_calculado:.8f}")
print(f"Valor real esperado (Scipy):    0.45041653")

# Verificamos la altura mínima con nuestro gamma calculado
if gamma_calculado:
    h = 2.5
    a = 3.0
    y_min = (1 / gamma_calculado) * (1 - np.cosh(gamma_calculado * a)) + h
    print(f"\nAltura del punto más bajo: {y_min:.4f} m")


# 3. Cálculo de la altura mínima (en x = 0)
y_min = (1 / gamma_calculado) * (1 - np.cosh(gamma_calculado * a)) + h
print(f"Altura del punto más bajo de la soga: {y_min:.4f} m")

# 4. Generación de los puntos para graficar
x = np.linspace(-a, a, 200) # 200 puntos entre los dos postes
y = (1 / gamma_calculado) * (np.cosh(gamma_calculado * x) - np.cosh(gamma_calculado * a)) + h

# 5. Configuración de la Gráfica
fig, ax = plt.subplots(figsize=(8, 5))

# Dibujar la soga
ax.plot(x, y, color='blue', linewidth=2.5, label='Soga (Catenaria)')

# Dibujar los postes
ax.plot([-a, -a], [0, h], color='black', linestyle='--', linewidth=2, label='Postes')
ax.plot([a, a], [0, h], color='black', linestyle='--', linewidth=2)

# Marcar el suelo
ax.axhline(0, color='gray', linewidth=1.5, label='Suelo')

# Marcar los puntos de amarre (postes)
ax.plot([-a, a], [h, h], 'ro', markersize=6, label='Puntos de amarre')

# Marcar el punto más bajo
ax.plot(0, y_min, 'go', markersize=8, label=f'Mínimo ({y_min:.2f} m)')

# Detalles estéticos
ax.set_title('Perfil de la soga suspendida (Catenaria)', fontsize=14)
ax.set_xlabel('Distancia horizontal $x$ [m]', fontsize=12)
ax.set_ylabel('Altura $y$ [m]', fontsize=12)
ax.grid(True, linestyle=':', alpha=0.7)
ax.legend(loc='lower right')
ax.set_aspect('equal') # Esto es crucial para que la soga no se vea deformada

plt.savefig('tp2a.png', dpi=300)
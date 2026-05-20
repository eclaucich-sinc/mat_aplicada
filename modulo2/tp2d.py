import numpy as np

# 1. Parámetros del problema
L = 8.0
h = 2.5

# 2. Cálculo analítico del gamma límite (condición de toque)
gamma_lim = (2 * h) / ((L / 2)**2 - h**2)

# 3. Función a la que le buscaremos la raíz: f(a) = 0
def f_a(a):
    return np.cosh(gamma_lim * a) - (1 + h * gamma_lim)

# 4. Implementación del Método de Bisección
def biseccion(func, lim_inf, lim_sup, tol_error):
    # Verificamos cambio de signo (Bolzano)
    if func(lim_inf) * func(lim_sup) > 0:
        raise ValueError("El intervalo inicial no garantiza una raíz.")
        
    a_n = lim_inf
    b_n = lim_sup
    n = 0
    
    print(f"{'Iter':<5} | {'Extremo Izq':<12} | {'Extremo Der':<12} | {'Medio (a_aprox)':<15} | {'Error Maximo':<15}")
    print("-" * 68)
    
    # El ciclo continúa mientras el error máximo del intervalo sea mayor a la tolerancia
    while (b_n - a_n) / 2.0 > tol_error:
        c_n = (a_n + b_n) / 2.0
        error_actual = (b_n - a_n) / 2.0
        print(f"{n:<5} | {a_n:<12.6f} | {b_n:<12.6f} | {c_n:<15.6f} | {error_actual:<15.6f}")
        
        # Evaluamos el punto medio
        if func(c_n) == 0:
            return c_n # Encontramos la raíz exacta de casualidad
        elif func(lim_inf) * func(c_n) < 0:
            b_n = c_n # La raíz está en la mitad izquierda
        else:
            a_n = c_n # La raíz está en la mitad derecha
            
        n += 1
        
    # Calculamos el valor final que cumple la tolerancia
    c_final = (a_n + b_n) / 2.0
    error_final = (b_n - a_n) / 2.0
    print(f"{n:<5} | {a_n:<12.6f} | {b_n:<12.6f} | {c_final:<15.6f} | {error_final:<15.6f}")
    
    return c_final

# --- EJECUCIÓN ---

# Sabemos que con a=3 la soga no tocaba (y > 0). 
# Si acercamos los postes a a=2, cuelga por debajo de 0 (f(2) < 0).
# Usamos el intervalo inicial [2.0, 3.0]

# Tolerancia en 'a' = 0.5 mm para que en '2a' sea 1 mm
tolerancia = 0.0005 

a_calculado = biseccion(f_a, 2.0, 3.0, tolerancia)
distancia_total = 2 * a_calculado

print("-" * 68)
print(f"Conclusión:")
print(f"Distancia del centro al poste (a): {a_calculado:.4f} m")
print(f"Separación total entre postes (2a): {distancia_total:.4f} m")
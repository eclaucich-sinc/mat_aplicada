import numpy as np

# Reutilizamos el gamma y el 'a' que calculamos en el inciso anterior
gamma_sol = 0.45041653  
a = 3.0

# Definimos la función integrando de la longitud de arco
# f(x) = sqrt(1 + (y'(x))^2) = cosh(gamma * x)
def integrando(x):
    return np.cosh(gamma_sol * x)

# Implementación del Método de Simpson 1/3
def simpson_13(func, lim_inf, lim_sup, n_intervalos):
    """
    func: Función a integrar
    lim_inf, lim_sup: Límites de integración [a, b]
    n_intervalos: Cantidad de subintervalos (debe ser un número par)
    """
    if n_intervalos % 2 != 0:
        raise ValueError("El número de intervalos debe ser par para Simpson 1/3.")
        
    h = (lim_sup - lim_inf) / n_intervalos
    x = np.linspace(lim_inf, lim_sup, n_intervalos + 1)
    y = func(x)
    
    # Aplicamos la fórmula: (h/3) * (y0 + 4*(y1+y3+...) + 2*(y2+y4+...) + yn)
    suma = y[0] + y[-1]
    
    # Suma de los términos impares (multiplicados por 4)
    suma += 4 * np.sum(y[1:-1:2])
    
    # Suma de los términos pares (multiplicados por 2)
    suma += 2 * np.sum(y[2:-2:2])
    
    integral = (h / 3) * suma
    return integral

# --- EJECUCIÓN DEL CÁLCULO ---

# Usamos 100 intervalos (un número par razonable para excelente precisión)
n = 100 

longitud_calculada = simpson_13(integrando, -a, a, n)

print(f"Longitud de la soga mediante integración numérica (Simpson): {longitud_calculada:.8f} m")
print(f"Longitud teórica esperada: 8.00000000 m")
print(f"Error absoluto: {abs(8.0 - longitud_calculada):.2e} m")
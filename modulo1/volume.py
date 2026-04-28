import numpy as np
from scipy.integrate import nquad

def integrando(mu, nu):
    return np.sinh(mu) / (np.cosh(mu) - np.cos(nu))**3

# Límites de integración para mu y nu (no depende de phi)
limites = [
    [1, 2],                 # Límites para mu
    [-np.pi, np.pi],        # Límites para nu
]

# Calcular la integral
volumen, error = nquad(integrando, limites)

volumen = 2 * np.pi * volumen  # Integración sobre phi

print(f"Volumen calculado: {volumen:.5f}")
print(f"Error estimado: {error:.2e}")
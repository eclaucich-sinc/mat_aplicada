import numpy as np
import matplotlib.pyplot as plt

# 1. Parámetros y malla
a = 1.0
# Solo necesitamos barrer mu (entre las fronteras) y nu (ángulo polar modificado)
mu = np.linspace(1, 2, 150)
nu = np.linspace(-np.pi, np.pi, 150)
MU, NU = np.meshgrid(mu, nu)

# 2. Transformación al plano XZ (asumiendo phi = 0, por lo que cos(phi) = 1)
D = np.cosh(MU) - np.cos(NU)
X = (a * np.sinh(MU)) / D
Z = (a * np.sin(NU)) / D

# 3. Cálculo de la temperatura analítica
U = 60 * MU - 40

# 4. Configuración del gráfico
fig, ax = plt.subplots(figsize=(10, 8))

# Generar el mapa de calor relleno (contourf)
mapa_calor = ax.contourf(X, Z, U, levels=50, cmap='inferno')

# Agregar las líneas de contorno (curvas de nivel) sobre el mapa
lineas_nivel = ax.contour(X, Z, U, levels=10, colors='white', linewidths=0.5, alpha=0.5)

# Barra de colores
cbar = plt.colorbar(mapa_calor, ax=ax)
cbar.set_label('Temperatura u(μ) [°C]', rotation=270, labelpad=20)

# Ajustes estéticos fundamentales
ax.set_aspect('equal') # ¡Clave! Para que las circunferencias no se vean como elipses
ax.set_title('Corte Transversal 2D del Flujo de Calor\n(Plano XZ, simetría azimutal)', fontsize=14)
ax.set_xlabel('Distancia radial desde el eje Z (ρ)', fontsize=12)
ax.set_ylabel('Eje Z', fontsize=12)

# Opcional: Agregar texto para identificar las fronteras
#ax.text(1.2, 0, '$\mu=1$ (20°)', color='white', fontsize=10, ha='center', va='center', backgroundcolor='black')
#ax.text(1.05, 0, '$\mu=2$ (80°)', color='black', fontsize=10, ha='center', va='center', backgroundcolor='white')

plt.grid(True, linestyle='--', alpha=0.3)
plt.show()
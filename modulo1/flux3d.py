import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Conducción de Calor Toroidal", layout="wide")
st.title("Distribución de Temperatura en Conductor Toroidal")
st.markdown("""
Visualización del estado estacionario de conducción de calor en la región $\Omega$ ($1 \le \mu \le 2$).  
La temperatura sigue la ley: **$u(\mu) = 60\mu - 40$**
""")

# --- PARÁMETROS DEL SISTEMA ---
a = 1.0

# Ecuación de temperatura obtenida analíticamente
def temperatura(mu):
    return 60 * mu - 40

# Transformación de coordenadas
@st.cache_data
def toroidales_a_cartesianas(mu, nu_max, phi_max, resolucion):
    nu = np.linspace(-nu_max, nu_max, resolucion)
    phi = np.linspace(0, phi_max, resolucion)
    NU, PHI = np.meshgrid(nu, phi)
    
    D = np.cosh(mu) - np.cos(NU) + 1e-9
    X = (a * np.sinh(mu) * np.cos(PHI)) / D
    Y = (a * np.sinh(mu) * np.sin(PHI)) / D
    Z = (a * np.sin(NU)) / D
    return X, Y, Z

# --- PANEL LATERAL ---
st.sidebar.header("Controles de Visualización")

corte_transversal = st.sidebar.checkbox("Activar corte transversal (Media dona)", value=True, 
                                        help="Permite ver las capas interiores.")
phi_limite = np.pi if corte_transversal else 2 * np.pi

st.sidebar.markdown("---")
st.sidebar.subheader("Explorador Térmico")
mu_explorador = st.sidebar.slider(
    "Mover capa intermedia ($\mu$)", 
    min_value=1.0, max_value=2.0, value=1.5, step=0.05,
    help="Desliza para ver la temperatura en el interior del sólido."
)

st.sidebar.info(f"**Temperatura en la capa seleccionada:**\n\nu({mu_explorador:.2f}) = {temperatura(mu_explorador):.1f}°")

# --- CONSTRUCCIÓN DEL GRÁFICO ---
fig = go.Figure()
escala_termica = 'Inferno' # Escala de colores que va de oscuro/frío a claro/caliente

def agregar_capa_termica(mu_val, opacidad, nombre, mostrar_escala=False):
    X, Y, Z = toroidales_a_cartesianas(mu_val, np.pi, phi_limite, 80)
    
    # Creamos una matriz del mismo tamaño que X, pero llena con el valor de la temperatura
    T = np.full_like(X, temperatura(mu_val))
    
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        surfacecolor=T,             # El color depende de la matriz de temperatura
        colorscale=escala_termica,
        cmin=20, cmax=80,           # Fijamos los límites de la barra de color según el TP
        opacity=opacidad,
        name=nombre,
        showscale=mostrar_escala,   # Solo mostramos la barra de color una vez
        colorbar=dict(title="Temperatura (u)", x=0.9) if mostrar_escala else None,
        hovertemplate='μ: ' + str(round(mu_val, 2)) + '<br>Temperatura: %{surfacecolor:.1f}<extra></extra>'
    ))

# 1. Frontera Exterior (Fría)
agregar_capa_termica(1.0, 0.2 if mu_explorador > 1.0 else 1.0, "Frontera Ext (μ=1, u=20)", mostrar_escala=True)

# 2. Frontera Interior (Caliente)
agregar_capa_termica(2.0, 1.0, "Frontera Int (μ=2, u=80)")

# 3. Capa Exploradora (Intermedia)
if 1.0 < mu_explorador < 2.0:
    agregar_capa_termica(mu_explorador, 0.9, f"Capa (μ={mu_explorador:.2f})")

# --- AJUSTES FINALES ---
fig.update_layout(
    scene=dict(
        xaxis=dict(title='Eje X', range=[-3, 3]),
        yaxis=dict(title='Eje Y', range=[-3, 3]),
        zaxis=dict(title='Eje Z', range=[-3, 3]),
        aspectmode='cube' 
    ),
    margin=dict(l=0, r=0, b=0, t=40),
    height=750,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

# Renderizar
st.plotly_chart(fig, use_container_width=True)
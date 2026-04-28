import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración básica de la página
st.set_page_config(page_title="Visor Toroidal Dual", layout="wide")
st.title("Visualizador Interactivo Dual de Coordenadas Toroidales")
st.markdown("""
Esta herramienta permite visualizar simultáneamente las superficies donde una coordenada es constante.
La intersección de estas superficies (junto con un plano de $\phi$ constante) define un punto en el espacio.
""")

# --- FUNCIÓN DE TRANSFORMACIÓN ---
def toroidales_a_cartesianas(mu, nu, phi, a):
    # Añadimos un pequeño epsilon para evitar división por cero si cosh(mu) == cos(nu) (en mu=0, nu=0)
    denominador = np.cosh(mu) - np.cos(nu) + 1e-9
    x = (a * np.sinh(mu) * np.cos(phi)) / denominador
    y = (a * np.sinh(mu) * np.sin(phi)) / denominador
    z = (a * np.sin(nu)) / denominador
    return x, y, z

# --- PANEL LATERAL CON CONTROLES ---
st.sidebar.header("Parámetros Globales")
a = st.sidebar.slider("Parámetro 'a' (Radio del anillo focal)", min_value=0.5, max_value=3.0, value=1.0, step=0.1)
resolucion = st.sidebar.slider("Resolución de malla", 30, 150, 80, step=10, help="Mayor resolución = gráficos más suaves pero más lentos.")

st.sidebar.markdown("---")

# --- SECCIÓN DEL TORO (MU CONSTANTE) ---
st.sidebar.subheader("1. Superficie de $\mu$ Constante (Toro)")
show_torus = st.sidebar.checkbox("Mostrar Toro", value=True)
mu_val = st.sidebar.slider("Valor fijo de $\mu$", 0.1, 4.0, 1.0, 0.1, key="mu_fixed", help="μ pequeño = toro grueso, μ grande = toro delgado")
opacity_torus = st.sidebar.slider("Opacidad Toro", 0.0, 1.0, 0.6, key="op_tor")

with st.sidebar.expander("Rángos de barrido del Toro"):
    nu_max_t = st.slider("Barrido de $\nu$ (sección circular)", 0.1, np.pi, np.pi, key="nu_sweep_t")
    phi_max_t = st.slider("Barrido de $\phi$ (rotación)", 0.1, 2*np.pi, 2*np.pi, key="phi_sweep_t")

st.sidebar.markdown("---")

# --- SECCIÓN DE LA ESFERA (NU CONSTANTE) ---
st.sidebar.subheader("2. Superficie de $\nu$ Constante (Esfera Excéntrica)")
show_sphere = st.sidebar.checkbox("Mostrar Esfera", value=True)
nu_val = st.sidebar.slider("Valor fijo de $\nu$", -np.pi, np.pi, np.pi/2, 0.1, key="nu_fixed", help="v > 0 arriba del plano xy, v < 0 abajo")
opacity_sphere = st.sidebar.slider("Opacidad Esfera", 0.0, 1.0, 0.7, key="op_sph")

with st.sidebar.expander("Rángos de barrido de la Esfera"):
    mu_max_s = st.slider("Barrido máximo de $\mu$", 0.5, 5.0, 2.5, key="mu_sweep_s", help="Controla qué tan lejos se extiende la esfera hacia afuera")
    phi_max_s = st.slider("Barrido de $\phi$ (rotación)", 0.1, 2*np.pi, 2*np.pi, key="phi_sweep_s")

# --- GENERACIÓN DE DATOS Y GRÁFICO ---
fig = go.Figure()

# 1. Generar y agregar el Toro
if show_torus:
    # Creamos mallas específicas para el toro
    nu_t = np.linspace(-nu_max_t, nu_max_t, resolucion)
    phi_t = np.linspace(0, phi_max_t, resolucion)
    NU_T, PHI_T = np.meshgrid(nu_t, phi_t)
    
    Xt, Yt, Zt = toroidales_a_cartesianas(1.0, NU_T, PHI_T, a)
    
    fig.add_trace(go.Surface(
        x=Xt, y=Yt, z=Zt, 
        colorscale='Blues', 
        opacity=opacity_torus, 
        showscale=False, 
        name=f'Toro (μ={mu_val:.1f})',
        hovertemplate='μ fijo<br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>'
    ))

    Xt, Yt, Zt = toroidales_a_cartesianas(2.0, NU_T, PHI_T, a)
    
    fig.add_trace(go.Surface(
        x=Xt, y=Yt, z=Zt, 
        colorscale='Greens', 
        opacity=opacity_torus, 
        showscale=False, 
        name=f'Toro (μ={mu_val:.1f})',
        hovertemplate='μ fijo<br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>'
    ))

# 2. Generar y agregar la Esfera
if show_sphere:
    # Creamos mallas específicas para la esfera (mu empieza en 0.01 para evitar singularidades)
    mu_s = np.linspace(0.01, mu_max_s, resolucion)
    phi_s = np.linspace(0, phi_max_s, resolucion)
    MU_S, PHI_S = np.meshgrid(mu_s, phi_s)
    
    Xs, Ys, Zs = toroidales_a_cartesianas(MU_S, nu_val, PHI_S, a)
    
    fig.add_trace(go.Surface(
        x=Xs, y=Ys, z=Zs, 
        colorscale='Reds', 
        opacity=opacity_sphere, 
        showscale=False, 
        name=f'Esfera (ν={nu_val:.2f})',
        hovertemplate='ν fijo<br>X: %{x:.2f}<br>Y: %{y:.2f}<br>Z: %{z:.2f}<extra></extra>'
    ))

# --- CONFIGURACIÓN DEL DISEÑO 3D ---
# Calculamos límites dinámicos basados en 'a' y mu_max_s para que no se corte
dynamic_lim = max(a + 2, (a * np.sinh(2.0))/(np.cosh(2.0)-1) if show_sphere else a+1)
if show_sphere and mu_max_s < 1.0: # Ajuste si mu_max es muy pequeño (esfera gigante)
     dynamic_lim = (a * np.sinh(mu_s[0]))/(np.cosh(mu_s[0])-1) * 0.5 

fig.update_layout(
    scene=dict(
        xaxis=dict(title='Eje X', range=[-dynamic_lim, dynamic_lim]),
        yaxis=dict(title='Eje Y', range=[-dynamic_lim, dynamic_lim]),
        zaxis=dict(title='Eje Z', range=[-dynamic_lim, dynamic_lim]),
        # aspectmode='data' es CRUCIAL para geometría real
        aspectmode='data' 
    ),
    margin=dict(l=0, r=0, b=0, t=30),
    height=800,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)

# Mostrar en Streamlit
st.plotly_chart(fig, use_container_width=True)
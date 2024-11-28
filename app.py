import streamlit as st
from mc import run as mc_run
from pipe import run as pipe_run

# Sidebar para seleccionar método
method = st.sidebar.selectbox(
    "Seleccione el método de generación",
    ["Generación de datos (Montecarlo)", "Simulaciones"]
)

# Lógica para cambiar el método
if method == "Generación de datos (Montecarlo)":
    st.title('Generación de datos (Montecarlo)')
    mc_run()

if method == "Método Congruencial Lineal":
    st.title('Simulaciones')
    pipe_run()
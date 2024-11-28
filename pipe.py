import streamlit as st
import pandas as pd

def run():
    st.title('Simulaciones de Producción')
    
    # Sección de límites de litros por máquina
    st.subheader('Límite de Litros por Máquina')
    col1, col2, col3 = st.columns(3)
    with col1:
        m1_litros = st.number_input('M1 (Litros)', min_value=0.0, step=0.1, format="%.2f")
    with col2:
        m2_litros = st.number_input('M2 (Litros)', min_value=0.0, step=0.1, format="%.2f")
    with col3:
        m3_litros = st.number_input('M3 (Litros)', min_value=0.0, step=0.1, format="%.2f")
    
    # Sección de tiempos de limpieza por máquina
    st.subheader('Tiempo de Limpieza por Máquina (horas)')
    col4, col5, col6 = st.columns(3)
    with col4:
        m1_tiempo = st.number_input('M1 (horas)', min_value=0.0, step=0.1, format="%.2f")
    with col5:
        m2_tiempo = st.number_input('M2 (horas)', min_value=0.0, step=0.1, format="%.2f")
    with col6:
        m3_tiempo = st.number_input('M3 (horas)', min_value=0.0, step=0.1, format="%.2f")
    
    # Sección de carga de archivos CSV
    st.subheader('Cargar Archivos CSV del Monte Carlo')
    uploaded_files = st.file_uploader("Seleccione uno o más archivos CSV", accept_multiple_files=True, type=["csv"])
    if uploaded_files:
        for uploaded_file in uploaded_files:
            try:
                df = pd.read_csv(uploaded_file)
                st.write(f"Archivo cargado: {uploaded_file.name}")
                st.dataframe(df)
            except Exception as e:
                st.error(f"Error al leer el archivo {uploaded_file.name}: {e}")
    
    # Boton para iniciar simulación
    col7, col8, col9 = st.columns([1, 1, 1])
    with col8:
        if st.button('🛫 - Iniciar Simulación'):
            st.write('Simulación en progreso...')
            st.write('Simulación finalizada')
            st.write('Resultados:')
            st.write('Máquina 1:')
            st.write(f'Litros: {m1_litros}')
            st.write(f'Tiempo de limpieza: {m1_tiempo} horas')
            st.write('Máquina 2:')
            st.write(f'Litros: {m2_litros}')
            st.write(f'Tiempo de limpieza: {m2_tiempo} horas')
            st.write('Máquina 3:')
            st.write(f'Litros: {m3_litros}')
            st.write(f'Tiempo de limpieza: {m3_tiempo} horas')
    

if __name__ == "__main__":
    run()

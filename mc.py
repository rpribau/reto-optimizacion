import streamlit as st
import numpy as np
import pandas as pd
import random


class Dia:
    def __init__(self, id_dia: int, id_experimento: int, pedidos: float):
        self.id_dia = id_dia
        self.id_experimento = id_experimento
        self.pedidos = pedidos

    def __repr__(self):
        return f"Dia(id_dia={self.id_dia}, id_experimento={self.id_experimento}, pedidos={self.pedidos})"

class SimulacionMonteCarlo:
    def __init__(self):
        self.lista_de_pedidos = []

    def generar_valores_aleatorios(self,limite_inferior: float, limite_superior: float, número_de_dias: int, total_experimentos: int):
        lista_salida = []

        for i in range(total_experimentos):
            for j in range(número_de_dias):
                valor =  limite_inferior + random.random() * (limite_superior - limite_inferior)
                dia = Dia(j, i, valor)
                lista_salida.append(dia)

        return lista_salida

    def calcular_valores_media_varianza(self,lista_entrada, total_experimentos, seleccionado):

        suma_parcial = 0
        lista_parcial = []
        suma=0
        contador=0
        lista_dias=[]

        for i in range(total_experimentos):

            lista_filtrada = [dia for dia in lista_entrada if dia.id_experimento == i]

            if lista_filtrada:

                lista_filtrada.sort(key=lambda x: x.pedidos)

                # se selecciona el pedido del cliente
                dia_seleccionado = lista_filtrada[seleccionado]
                lista_parcial.append(dia_seleccionado)
                suma_parcial += dia_seleccionado.pedidos
                lista_dias.append(dia_seleccionado.pedidos)

        media = suma_parcial / total_experimentos if total_experimentos > 0 else 0

        # Calcular la varianza
        for dia in lista_parcial:
            suma = suma+ (dia.pedidos) ** 2
            contador +=1
        varianza= suma / (contador * (contador - 1)) - (media**2) / (contador - 1)

        return media, varianza,lista_dias

    def monte_carlo(self, limite_inferior: float, limite_superior: float, número_de_clientes: int, total_experimentos: int, seleccionado: int):
        self.lista_clientes = self.generar_valores_aleatorios(limite_inferior, limite_superior, número_de_clientes, total_experimentos)
        media, varianza,lista_parcial = self.calcular_valores_media_varianza(self.lista_clientes, total_experimentos, seleccionado)

        return [media, varianza,lista_parcial]

def obtener_datos(limite_inferior,limite_superior,enfoque):
    dias=5
    total_experimentos=100
    simulacion = SimulacionMonteCarlo()
    resultado = simulacion.monte_carlo(limite_inferior, limite_superior, dias, total_experimentos, enfoque)
    print(f"Media: {resultado[0]}, Varianza: {resultado[1]}")
    return resultado[0]

def obtener_datos2(limite_inferior,limite_superior,enfoque,enfoque2):
    dias=5
    total_experimentos=100
    simulacion = SimulacionMonteCarlo()
    resultado = simulacion.monte_carlo(limite_inferior, limite_superior, dias, total_experimentos, enfoque)
    print(f"Media: {resultado[0]}, Varianza: {resultado[1]}")
    if enfoque2 == 0: 
        return resultado[0]*1.1
    if enfoque2 == 1: 
        return resultado[0]*1.2
    if enfoque2 == 2: 
        return resultado[0]*1.3
    if enfoque2 == 3: 
        return resultado[0]*1.4
    if enfoque2 == 4: 
        return resultado[0]*1.5

def run():
    st.header("Simulación de Producción de Salsas")
    
    st.header("Configuración de Salsa Verde")
    col1, col2, col3 = st.columns(3)
    
    # Salsa Verde parameters
    with col1:
        st.subheader("Chico")
        verde_chica_min = st.number_input("Límite inferior chica verde", value=100.0, key="verde_chica_min")
        verde_chica_max = st.number_input("Límite superior chica verde", value=140.0, key="verde_chica_max")
        
    with col2:
        st.subheader("Mediano")
        verde_med_min = st.number_input("Límite inferior mediana verde", value=80.0, key="verde_med_min")
        verde_med_max = st.number_input("Límite superior mediana verde", value=120.0, key="verde_med_max")
        
    with col3:
        st.subheader("Grande")
        verde_grande_min = st.number_input("Límite inferior grande verde", value=60.0, key="verde_grande_min")
        verde_grande_max = st.number_input("Límite superior grande verde", value=100.0, key="verde_grande_max")

    st.header("Configuración de Salsa Roja")
    col4, col5, col6 = st.columns(3)
    
    # Salsa Roja parameters
    with col4:
        st.subheader("Chico")
        roja_chica_min = st.number_input("Límite inferior chica roja", value=50.0, key="roja_chica_min")
        roja_chica_max = st.number_input("Límite superior chica roja", value=70.0, key="roja_chica_max")
        
    with col5:
        st.subheader("Mediano")
        roja_med_min = st.number_input("Límite inferior mediana roja", value=40.0, key="roja_med_min")
        roja_med_max = st.number_input("Límite superior mediana roja", value=60.0, key="roja_med_max")
        
    with col6:
        st.subheader("Grande")
        roja_grande_min = st.number_input("Límite inferior grande roja", value=30.0, key="roja_grande_min")
        roja_grande_max = st.number_input("Límite superior grande roja", value=50.0, key="roja_grande_max")

    st.header("Configuración de Herramentales")
    col7, col8 = st.columns(2)
    
    # Herramentales parameters
    with col7:
        st.subheader("Herramental 1")
        herr1_min = st.number_input("Límite inferior herramental 1", value=0.0, key="herr1_min")
        herr1_max = st.number_input("Límite superior herramental 1", value=12.0, key="herr1_max")
        
    with col8:
        st.subheader("Herramental 2")
        herr2_min = st.number_input("Límite inferior herramental 2", value=0.0, key="herr2_min")
        herr2_max = st.number_input("Límite superior herramental 2", value=12.0, key="herr2_max")

    # Enfoque selector
    st.header("Configuración de Enfoque")
    enfoque = st.select_slider(
        'Seleccione el enfoque',
        options=[0, 1, 2, 3, 4],
        value=2,
        help="0: Optimista, 2: Normal, 4: Pesimista"
    )

    if st.button("Ejecutar Simulación"):
        # Execute your simulation with the selected parameters
        simulacion = SimulacionMonteCarlo()
        
        # Generate data for salsa verde
        demandas_salsa_chica_verde = [obtener_datos2(verde_chica_min, verde_chica_max, enfoque,j) 
                              for i in range(5) 
                              for j in ([0] * 2 + [2] + [4] * 2)[i:i+1]]

        demandas_salsa_mediana_verde = [obtener_datos2(verde_med_min, verde_med_max, enfoque,j) 
                                for i in range(5) 
                                for j in ([0] * 2 + [2] + [4] * 2)[i:i+1]]

        demandas_salsa_grande_verde = [obtener_datos2(verde_grande_min, verde_grande_max, enfoque,j) 
                               for i in range(5) 
                               for j in ([0] * 2 + [2] + [4] * 2)[i:i+1]]

        
        # Generate data for salsa roja
        demandas_salsa_chica_roja = [obtener_datos2(roja_chica_min, roja_chica_max, enfoque,j) 
                              for i in range(5) 
                              for j in ([0] * 2 + [2] + [4] * 2)[i:i+1]]

        demandas_salsa_mediana_roja = [obtener_datos2(roja_med_min, roja_med_max, enfoque,j) 
                                for i in range(5) 
                                for j in ([0] * 2 + [2] + [4] * 2)[i:i+1]]

        demandas_salsa_grande_roja = [obtener_datos2(roja_grande_min, roja_grande_max, enfoque,j) 
                               for i in range(5) 
                               for j in ([0] * 2 + [2] + [4] * 2)[i:i+1]]

        
        # Generate data for herramentales
        llegada_herramental1 = [obtener_datos(herr1_min, herr1_max, enfoque) for _ in range(5)]
        llegada_herramental2 = [obtener_datos(herr2_min, herr2_max, enfoque) for _ in range(5)]

        # Create and display DataFrames
        df_verde = pd.DataFrame({
            'Tamaño chico verde': demandas_salsa_chica_verde,
            'Tamaño mediano verde': demandas_salsa_mediana_verde,
            'Tamaño grande verde': demandas_salsa_grande_verde
        })

        df_roja = pd.DataFrame({
            'Tamaño chico roja': demandas_salsa_chica_roja,
            'Tamaño mediano roja': demandas_salsa_mediana_roja,
            'Tamaño grande roja': demandas_salsa_grande_roja
        })

        df_herramentales = pd.DataFrame({
            'Herramental 1': llegada_herramental1,
            'Herramental 2': llegada_herramental2
        })

        # Descargar resultados de salsa verde, salsa roja y herramentales
        # Nombres: salsa_verde.csv, salsa_roja.csv, herramentales.csv
        df_verde.to_csv("salsa_verde.csv", index=False)
        df_roja.to_csv("salsa_roja.csv", index=False)
        df_herramentales.to_csv("herramentales.csv", index=False)
        

        st.header("Resultados")
        st.subheader("Salsa Verde")
        st.dataframe(df_verde, width=900)
        
        st.subheader("Salsa Roja")
        st.dataframe(df_roja, width=900)
        
        st.subheader("Herramentales")
        st.dataframe(df_herramentales, width=900)

if __name__ == "__main__":
    run()

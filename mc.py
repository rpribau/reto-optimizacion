import streamlit as st
import numpy as np
import pandas as pd
import streamlit as st
import pandas as pd
import random
import numpy as np

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

    def generar_valores_aleatorios(self, limite_inferior: float, limite_superior: float, numero_de_dias: int, total_experimentos: int):
        lista_salida = []
        for i in range(total_experimentos):
            for j in range(numero_de_dias):
                valor = limite_inferior + random.random() * (limite_superior - limite_inferior)
                dia = Dia(j, i, valor)
                lista_salida.append(dia)
        return lista_salida

    def calcular_valores_media_varianza(self, lista_entrada, total_experimentos, seleccionado):
        suma_parcial = 0
        lista_parcial = []
        lista_dias = []

        for i in range(total_experimentos):
            lista_filtrada = [dia for dia in lista_entrada if dia.id_experimento == i]
            if lista_filtrada:
                lista_filtrada.sort(key=lambda x: x.pedidos)
                dia_seleccionado = lista_filtrada[seleccionado]
                lista_parcial.append(dia_seleccionado)
                suma_parcial += dia_seleccionado.pedidos
                lista_dias.append(dia_seleccionado.pedidos)

        media = suma_parcial / total_experimentos if total_experimentos > 0 else 0
        varianza = np.var(lista_dias) if len(lista_dias) > 1 else 0
        return media, varianza, lista_dias

    def monte_carlo(self, limite_inferior: float, limite_superior: float, numero_de_dias: int, total_experimentos: int, seleccionado: int):
        self.lista_clientes = self.generar_valores_aleatorios(limite_inferior, limite_superior, numero_de_dias, total_experimentos)
        media, varianza, lista_parcial = self.calcular_valores_media_varianza(self.lista_clientes, total_experimentos, seleccionado)
        return [media, varianza, lista_parcial]

def obtener_datos(limite_inferior, limite_superior, enfoque,dias):
    total_experimentos = 100
    simulacion = SimulacionMonteCarlo()
    resultado = simulacion.monte_carlo(limite_inferior, limite_superior, dias, total_experimentos, enfoque)

    return resultado[0]
def run():
    st.subheader('Montecarlo')
    
    st.title("Simulación de Monte Carlo para la llegada de Herramentales")

    limite_inferior = st.number_input("Límite inferior", min_value=0.0, max_value=24.0, value=0.0,step=1.0)
    limite_superior = st.number_input("Límite superior", min_value=1.0, max_value=24.0, value=12.0,step=1.0)

    enfoque = st.slider("Enfoque", min_value=0, max_value=4, value=2, step=1)
    enfoque2 = st.slider("Enfoque segundo Herramental", min_value=0, max_value=4, value=2, step=1)


    numero_de_dias=5
    llegada_herramental1= []
    for i in range(numero_de_dias):
        limite_inferior=0.0
        limite_superior=12.0
        valor=obtener_datos(limite_inferior,limite_superior,enfoque,numero_de_dias)
        llegada_herramental1.append(valor)

    numero_de_dias=5
    llegada_herramental2= []
    for i in range(numero_de_dias):
        limite_inferior=0.0
        limite_superior=12.0
        valor=obtener_datos(limite_inferior,limite_superior,enfoque2,numero_de_dias)
        llegada_herramental2.append(valor)


    st.subheader("Resultados")
    df_resultados = pd.DataFrame({
        "Herramental 1": llegada_herramental1,
        "Herramental 2": llegada_herramental2,
    })
    st.dataframe(df_resultados)

    st.download_button("Descargar resultados", df_resultados.to_csv(index=False), "resultados.csv", "text/csv")


if __name__ == "__main__":
    run()
import streamlit as st
import pandas as pd
from datetime import timedelta
import plotly.figure_factory as ff
import plotly.graph_objs as go



def run():
    # Título de la App
    st.title("Secuenciación de Producción de Salsas")

    # Sección de Parámetros Editables
    st.sidebar.header("Parámetros de Configuración")
    st.sidebar.subheader("Rates de Producción (litros/hora)")
    rM1 = st.sidebar.number_input("Rate Máquina 1 (rM1)", min_value=50, max_value=500, value=230, step=10)
    rM2 = st.sidebar.number_input("Rate Máquina 2 (rM2)", min_value=50, max_value=500, value=290, step=10)
    rM3 = st.sidebar.number_input("Rate Máquina 3 (rM3)", min_value=50, max_value=500, value=200, step=10)

    st.sidebar.subheader("Capacidades Máximas (litros)")
    capacidad_max_M1 = st.sidebar.number_input("Capacidad Máxima M1", min_value=100, max_value=500, value=345, step=10)
    capacidad_max_M2 = st.sidebar.number_input("Capacidad Máxima M2", min_value=100, max_value=500, value=435, step=10)
    capacidad_max_M3 = st.sidebar.number_input("Capacidad Máxima M3", min_value=100, max_value=500, value=300, step=10)

    st.sidebar.subheader("Capacidades Mínimas (litros)")
    capacidad_min_M1 = st.sidebar.number_input("Capacidad Mínima M1", min_value=10, max_value=100, value=20, step=5)
    capacidad_min_M2 = st.sidebar.number_input("Capacidad Mínima M2", min_value=10, max_value=100, value=40, step=5)
    capacidad_min_M3 = st.sidebar.number_input("Capacidad Mínima M3", min_value=10, max_value=100, value=80, step=5)

    u = 0.25  # Tiempo fijo de limpieza en horas

    # Espacios para cargar los DataFrames
    st.subheader("Cargar DataFrames")

    # DataFrame para `salsa_verde`
    st.write("**Salsa Verde**")
    salsa_verde_file = st.file_uploader("Subir archivo CSV para Salsa Verde", type="csv", key="salsa_verde")
    if salsa_verde_file:
        salsa_verde = pd.read_csv(salsa_verde_file)
        # Crear columnas de producción para Salsa Verde
        salsa_verde['Produccion chico'] = salsa_verde['Tamaño chico verde'].astype(float) * 0.9
        salsa_verde['Produccion mediano'] = salsa_verde['Tamaño mediano verde'].astype(float) * 1.5
        salsa_verde['Produccion grande'] = salsa_verde['Tamaño grande verde'].astype(float) * 3
        salsa_verde['Litros totales'] = salsa_verde['Produccion chico'] + salsa_verde['Produccion mediano'] + salsa_verde['Produccion grande']
        st.write(salsa_verde)
    else:
        st.info("Por favor, carga un archivo CSV para Salsa Verde.")

    # DataFrame para `salsa_roja`
    st.write("**Salsa Roja**")
    salsa_roja_file = st.file_uploader("Subir archivo CSV para Salsa Roja", type="csv", key="salsa_roja")
    if salsa_roja_file:
        salsa_roja = pd.read_csv(salsa_roja_file)
        # Crear columnas de producción para Salsa Roja
        salsa_roja['Produccion chico'] = salsa_roja['Tamaño chico roja'].astype(float) * 0.3
        salsa_roja['Produccion mediano'] = salsa_roja['Tamaño mediano roja'].astype(float) * 0.5
        salsa_roja['Produccion grande'] = salsa_roja['Tamaño grande roja'].astype(float) * 1.0
        salsa_roja['Litros totales'] = salsa_roja['Produccion chico'] + salsa_roja['Produccion mediano'] + salsa_roja['Produccion grande']
        st.write(salsa_roja)
    else:
        st.info("Por favor, carga un archivo CSV para Salsa Roja.")

    # DataFrame para `df3` (herramentales)
    st.write("**DataFrame de Herramentales (df3)**")
    df3_file = st.file_uploader("Subir archivo CSV para Herramentales (df3)", type="csv", key="df3")
    if df3_file:
        df3 = pd.read_csv(df3_file)
        st.write(df3)
    else:
        st.info("Por favor, carga un archivo CSV para Herramentales (df3).")

    # Seleccionar el Día antes de calcular
    if salsa_verde_file and salsa_roja_file and df3_file:
        dia = st.number_input("Seleccionar Día", min_value=0, max_value=len(df3) - 1, step=1)
    else:
        st.warning("Por favor, carga todos los DataFrames antes de seleccionar el Día.")

    # Función para calcular la secuenciación
    def calcular_secuenciacion_por_dia(dia, df3, salsa_verde, salsa_roja, rM1, rM2, rM3, u):
        def convertir_horas(horas_decimal):
            """
            Convierte un valor de horas en formato decimal a una cadena 'HH:MM', 
            manejando correctamente cuando los minutos son 60 o mayores.
            """
            horas_base = int(horas_decimal)
            minutos_decimal = (horas_decimal - horas_base) * 60
            
            # Ajustar horas y minutos
            minutos = int(minutos_decimal)
            horas_adicionales = minutos // 60
            minutos_finales = minutos % 60
            horas_totales = horas_base + horas_adicionales
            
            return f"{horas_totales:02d}:{minutos_finales:02d}"

        def calcular_hora_real(horas_decimal):
            horas_base = 6
            tiempo_total = horas_base + horas_decimal
            return convertir_horas(tiempo_total)

        secuencias = []
        proceso_actual = 1

        herramental_dia = df3.loc[dia]
        if herramental_dia['Herramental 1'] <= herramental_dia['Herramental 2']:
            salsa_inicial = ("verde", salsa_verde, herramental_dia['Herramental 1'])
            salsa_posterior = ("roja", salsa_roja, herramental_dia['Herramental 2'])
        else:
            salsa_inicial = ("roja", salsa_roja, herramental_dia['Herramental 2'])
            salsa_posterior = ("verde", salsa_verde, herramental_dia['Herramental 1'])

        def secuenciar_salsa(salsa_actual, nombre_salsa, hora_herramental, proceso_actual):
            demanda = salsa_actual.loc[dia, 'Litros totales']
            xL = ((rM1 * rM2) * (hora_herramental - 2 * u)) / (rM1 + rM2)
            xL = min(xL, demanda)
            prod_M1 = (xL / rM1) + u
            prod_M2 = (xL / rM2) + u
            prod_M3 = (xL / rM3) + u

            h_inicio_M3 = hora_herramental
            hora_inicio_M1 = h_inicio_M3 - (prod_M1 + prod_M2)

            hora_fin_M1 = hora_inicio_M1 + prod_M1
            hora_fin_M2 = hora_fin_M1 + prod_M2
            hora_fin_M3 = hora_fin_M2 + prod_M3

            secuencias.append({
                "Proceso": proceso_actual,
                "Máquina": 1,
                "Producto": f"Salsa {nombre_salsa}",
                "Cantidad": xL,
                "Secuencia": f"{proceso_actual}.1",
                "Tiempo de proceso": round(prod_M1, 2),
                "Tiempo entre procesos": 0,
                "Hora Inicio": calcular_hora_real(hora_inicio_M1),
                "Hora Fin": calcular_hora_real(hora_fin_M1),
            })
            secuencias.append({
                "Proceso": proceso_actual,
                "Máquina": 2,
                "Producto": f"Salsa {nombre_salsa}",
                "Cantidad": xL,
                "Secuencia": f"{proceso_actual}.2",
                "Tiempo de proceso": round(prod_M2, 2),
                "Tiempo entre procesos": 1,
                "Hora Inicio": calcular_hora_real(hora_fin_M1),
                "Hora Fin": calcular_hora_real(hora_fin_M2),
            })
            secuencias.append({
                "Proceso": proceso_actual,
                "Máquina": 3,
                "Producto": f"Salsa {nombre_salsa}",
                "Cantidad": xL,
                "Secuencia": f"{proceso_actual}.3",
                "Tiempo de proceso": round(prod_M3, 2),
                "Tiempo entre procesos": 2,
                "Hora Inicio": calcular_hora_real(h_inicio_M3),
                "Hora Fin": calcular_hora_real(hora_fin_M3),
            })
            return hora_fin_M3

        nombre, salsa_actual, hora_herramental = salsa_inicial
        hora_fin = secuenciar_salsa(salsa_actual, nombre, hora_herramental, proceso_actual)

        if hora_fin < 18.0:
            proceso_actual += 1
            nombre_p, salsa_actual_p, hora_herramental_p = salsa_posterior
            start_time_p = max(hora_fin, hora_herramental_p)
            secuenciar_salsa(salsa_actual_p, nombre_p, start_time_p, proceso_actual)

        return pd.DataFrame(secuencias)

    def convertir_a_decimal(hora_str):
        """Convierte una hora en formato 'HH:MM' a formato decimal."""
        if not isinstance(hora_str, str) or ":" not in hora_str:
            return None  # Si no es una hora válida, devolver None
        horas, minutos = map(int, hora_str.split(":"))
        return horas + minutos / 60

    # Función para verificar errores en la secuenciación
    def verificar_errores_secuenciacion(df_resultado):
        # Agregar columnas auxiliares con las horas en formato decimal
        df_resultado['Hora Inicio Decimal'] = df_resultado['Hora Inicio'].apply(convertir_a_decimal)
        df_resultado['Hora Fin Decimal'] = df_resultado['Hora Fin'].apply(convertir_a_decimal)

        # Rango permitido (de 6:00 a 18:00 horas)
        hora_inicio_turno = 6
        hora_fin_turno = 18

        # Identificar filas fuera del rango
        errores = []
        for index, row in df_resultado.iterrows():
            if (row['Hora Inicio Decimal'] is None or 
                row['Hora Fin Decimal'] is None or 
                row['Hora Inicio Decimal'] < hora_inicio_turno or 
                row['Hora Fin Decimal'] > hora_fin_turno):
                error_msg = (f"Error en Proceso {row['Proceso']}, Máquina {row['Máquina']}: "
                             f"Hora Inicio {row['Hora Inicio']} (decimal: {row['Hora Inicio Decimal']:.2f}), "
                             f"Hora Fin {row['Hora Fin']} (decimal: {row['Hora Fin Decimal']:.2f})")
                errores.append(error_msg)

        return errores

    # Cálculo y visualización del resultado
    def convertir_a_decimal(hora_str):
        """Convierte una hora en formato 'HH:MM' a formato decimal."""
        if not isinstance(hora_str, str) or ":" not in hora_str:
            return None  # Si no es una hora válida, devolver None
        horas, minutos = map(int, hora_str.split(":"))
        return horas + minutos / 60

    # Función para verificar errores en la secuenciación
    def verificar_errores_secuenciacion(df_resultado):
        # Agregar columnas auxiliares con las horas en formato decimal
        df_resultado['Hora Inicio Decimal'] = df_resultado['Hora Inicio'].apply(convertir_a_decimal)
        df_resultado['Hora Fin Decimal'] = df_resultado['Hora Fin'].apply(convertir_a_decimal)

        # Rango permitido (de 6:00 a 18:00 horas)
        hora_inicio_turno = 6
        hora_fin_turno = 18

        # Identificar filas fuera del rango
        errores = []
        for index, row in df_resultado.iterrows():
            if (row['Hora Inicio Decimal'] is None or 
                row['Hora Fin Decimal'] is None or 
                row['Hora Inicio Decimal'] < hora_inicio_turno or 
                row['Hora Fin Decimal'] > hora_fin_turno):
                error_msg = (f"Error en Proceso {row['Proceso']}, Máquina {row['Máquina']}: "
                             f"Hora Inicio {row['Hora Inicio']} (decimal: {row['Hora Inicio Decimal']:.2f}), "
                             f"Hora Fin {row['Hora Fin']} (decimal: {row['Hora Fin Decimal']:.2f})")
                errores.append(error_msg)

        return errores


    # Cálculo y visualización del resultado
    if st.button("Calcular Secuenciación"):
        if salsa_verde_file and salsa_roja_file and df3_file:
            df_resultado = calcular_secuenciacion_por_dia(dia, df3, salsa_verde, salsa_roja, rM1, rM2, rM3, u)
            st.write("**Secuencia de Producción**")
            st.dataframe(df_resultado, width=900)

            # Verificar errores y mostrar
            errores = verificar_errores_secuenciacion(df_resultado)
            
            if errores:
                st.error("Se encontraron los siguientes errores en la secuenciación:")
                for error in errores:
                    st.warning(error)
            else:
                st.success("✅ No se encontraron errores en la secuenciación. Todos los procesos están dentro del rango de turno.")
            
            # Crear datos para el gráfico de Gantt
            gantt_data = []
            for _, row in df_resultado.iterrows():
                gantt_data.append({
                    'Task': f"M{row['Máquina']} ({row['Producto']})",
                    'Start': f"2024-01-01 {row['Hora Inicio']}:00",
                    'Finish': f"2024-01-01 {row['Hora Fin']}:00",
                    'Resource': row['Máquina']
                })

            # Crear gráfico Gantt
            fig = ff.create_gantt(
                gantt_data,
                index_col='Resource',  # Columna para los colores (en tu caso, Salsa verde/roja)
                show_colorbar=False,  # Desactiva la barra de colores
                group_tasks=True,
                title="Production Timeline",
                bar_width=0.3,
                showgrid_x=True,
                showgrid_y=True,
            )


            # Mostrar el gráfico en Streamlit
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Por favor, carga todos los DataFrames antes de realizar el cálculo.")


if __name__ == "__main__":
    run()

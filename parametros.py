import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Datos simulados
df = pd.DataFrame({
    "Año": [str(a) for a in range(2015, 2025)] * 5,
    "Provincia": ["AZUAY", "PICHINCHA", "GUAYAS", "LOJA", "MANABÍ"] * 10,
    "Tipo de Contratación": [
        "Subasta Inversa Electrónica",
        "Menor Cuantía",
        "Contratacion directa",
        "Catálogo electrónico - Mejor oferta",
        "Licitación"
    ] * 10,
    "Descripción": [
        "Adquisición de equipos informáticos",
        "Construcción de obras públicas",
        "Servicio de limpieza",
        "Compra de mobiliario",
        "Implementación de software"
    ] * 10
})

# Listas de selección
años = sorted(df["Año"].unique())
provincias = ["Todos"] + sorted(df["Provincia"].unique())
tipos_contratacion = ["Todos"] + sorted(df["Tipo de Contratación"].unique())

# Interfaz de usuario
st.title("Contrataciones Públicas")

col1, col2, col3 = st.columns(3)

with col1:
    anio = st.selectbox("Seleccione el año", ["Todos"] + años)

with col2:
    provincia = st.selectbox("Seleccione la provincia", provincias)

with col3:
    tipo = st.selectbox("Tipo de contratación", tipos_contratacion)

# Elegir librería de gráficos
grafico_tipo = st.radio("Seleccione el tipo de gráficos que desea visualizar:", ["Matplotlib", "Plotly"])

# Filtrado del DataFrame
df_filtrado = df.copy()

if anio != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Año"] == anio]

if provincia != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Provincia"] == provincia]

if tipo != "Todos":
    df_filtrado = df_filtrado[df_filtrado["Tipo de Contratación"] == tipo]

# Mostrar resultados
if not df_filtrado.empty:
    st.success(f"{len(df_filtrado)} registros encontrados:")
    st.dataframe(df_filtrado)

    if grafico_tipo == "Matplotlib":
        # Gráfico de Barras
        st.subheader("Gráfico de Barras por Año y Tipo de Contratación (Matplotlib)")
        fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
        df_filtrado.groupby(["Año", "Tipo de Contratación"]).size().unstack().plot(kind='bar', ax=ax_bar)
        ax_bar.set_title("Contrataciones por Año y Tipo")
        ax_bar.set_xlabel("Año")
        ax_bar.set_ylabel("Número de Contrataciones")
        st.pyplot(fig_bar)

        # Gráfico de Pastel
        st.subheader("Gráfico de Pastel por Provincia (Matplotlib)")
        provincia_counts = df_filtrado["Provincia"].value_counts()
        fig_pie, ax_pie = plt.subplots()
        ax_pie.pie(provincia_counts, labels=provincia_counts.index, autopct='%1.1f%%', startangle=90)
        ax_pie.axis('equal')
        st.pyplot(fig_pie)

        # Gráfico de Líneas
        st.subheader("Gráfico de Líneas por Año y Provincia (Matplotlib)")
        line_data = df_filtrado.groupby(["Año", "Provincia"]).size().unstack(fill_value=0)
        fig_line, ax_line = plt.subplots()
        line_data.plot(ax=ax_line, marker='o')
        ax_line.set_title("Evolución de Contrataciones por Año y Provincia")
        ax_line.set_xlabel("Año")
        ax_line.set_ylabel("Cantidad de Contrataciones")
        st.pyplot(fig_line)

    else:
        # Gráfico de Barras
        st.subheader("Gráfico de Barras por Año y Tipo de Contratación (Plotly)")
        bar_data = df_filtrado.groupby(["Año", "Tipo de Contratación"]).size().reset_index(name="Cantidad")
        fig_bar = px.bar(
            bar_data,
            x="Año",
            y="Cantidad",
            color="Tipo de Contratación",
            title="Contrataciones por Año y Tipo",
            barmode="group"
        )
        st.plotly_chart(fig_bar)

        # Gráfico de Pastel
        st.subheader("Gráfico de Pastel por Provincia (Plotly)")
        pie_data = df_filtrado["Provincia"].value_counts().reset_index()
        pie_data.columns = ["Provincia", "Cantidad"]
        fig_pie = px.pie(
            pie_data,
            names="Provincia",
            values="Cantidad",
            title="Distribución de Contrataciones por Provincia"
        )
        st.plotly_chart(fig_pie)

        # Gráfico de Líneas
        st.subheader("Gráfico de Líneas por Año y Provincia (Plotly)")
        line_data = df_filtrado.groupby(["Año", "Provincia"]).size().reset_index(name="Cantidad")
        fig_line = px.line(
            line_data,
            x="Año",
            y="Cantidad",
            color="Provincia",
            markers=True,
            title="Evolución de Contrataciones por Año y Provincia"
        )
        st.plotly_chart(fig_line)


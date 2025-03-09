import streamlit as st
import pandas as pd
import requests
import plotly.express as px

#  Configurar el Dashboard
st.set_page_config(page_title="Dashboard Económico", layout="wide")
st.title("Dashboard de Indicadores Económicos")

#  URLs de APIs públicas
URL_TIPO_CAMBIO = "https://api.exchangerate-api.com/v4/latest/MXN"  # Tipo de cambio MXN
URL_CRIPTO = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"  # BTC y ETH

#  Función para obtener datos de la API
def obtener_datos_api(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error al obtener datos de la API: {e}")
        return None

#  Obtener datos de tipo de cambio
cambio_data = obtener_datos_api(URL_TIPO_CAMBIO)

#  Procesar datos de tipo de cambio
if cambio_data and "rates" in cambio_data:
    df_cambio = pd.DataFrame(cambio_data["rates"], index=[0]).T.reset_index()

    #  Verificación del DataFrame
    st.write(" Columnas originales del DataFrame de tipo de cambio:", df_cambio.columns)

    #  Asegurar que tiene el formato correcto
    if df_cambio.shape[1] == 2:  # Aseguramos que solo haya dos columnas
        df_cambio.columns = ["Moneda", "Valor"]
    else:
        st.error(f"❌ Error: Se esperaban 2 columnas, pero se encontraron {df_cambio.shape[1]}.")
        st.dataframe(df_cambio)  # Mostrar DataFrame para depuración

   
    #  Mostrar tabla
    st.subheader(" Tabla de Tipo de Cambio")
    st.dataframe(df_cambio)

    # Gráfica de tendencia del Peso Mexicano
    st.subheader("Tendencia del Peso Mexicano")
    fig_mxn = px.line(df_cambio, x="Moneda", y="Valor", title="Tendencia del MXN frente a otras monedas")
    st.plotly_chart(fig_mxn)

else:
    st.error(" No se pudo obtener la información del tipo de cambio.")

# Obtener datos de criptomonedas (BTC y ETH)
cripto_data = obtener_datos_api(URL_CRIPTO)

# Procesar datos de criptomonedas
if cripto_data:
    bitcoin_precio = cripto_data.get("bitcoin", {}).get("usd", "N/A")
    ethereum_precio = cripto_data.get("ethereum", {}).get("usd", "N/A")

    st.subheader(" Precios de Criptomonedas")
    st.metric(label="Bitcoin (BTC)", value=f"${bitcoin_precio} USD")
    st.metric(label="Ethereum (ETH)", value=f"${ethereum_precio} USD")

    #  Gráfica de comparación BTC vs ETH
    st.subheader("Comparación de Bitcoin y Ethereum")
    df_cripto = pd.DataFrame({"Criptomoneda": ["Bitcoin", "Ethereum"], "Valor (USD)": [bitcoin_precio, ethereum_precio]})
    fig_cripto = px.bar(df_cripto, x="Criptomoneda", y="Valor (USD)", title="Comparación de Bitcoin y Ethereum")
    st.plotly_chart(fig_cripto)

else:
    st.error("No se pudo obtener la información de las criptomonedas.")


#Autor: Yael Sandoval

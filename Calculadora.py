import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

# =============================
# 1. CONFIGURACIÓN DE GOOGLE SHEETS
# =============================
scope = ["https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive"]

# Cargar credenciales desde Streamlit Secrets
creds_dict = json.loads(st.secrets["GOOGLE_CREDS"]["value"])
creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
client = gspread.authorize(creds)

# ID de tu hoja de Google Sheets
sheet_id = "1txRNRHgn-sn9YxXmS3NPA44ww-eYkZ6J14Yc0t3KyVE"
sheet = client.open_by_key(sheet_id).sheet1

# =============================
# 2. DISEÑO DE LA PÁGINA
# =============================
page_bg = """
<style>
[data-testid="stHeader"], 
[data-testid="stSidebar"], 
[data-testid="stMarkdownContainer"], 
[data-testid="stMetric"] {
    padding: 10px;
    border-radius: 10px;
}

/* Modo claro: fondo blanco, letras negras */
body[data-theme="light"] {
    background-color: #ffffff;
}
body[data-theme="light"] [data-testid="stHeader"],
body[data-theme="light"] [data-testid="stSidebar"],
body[data-theme="light"] [data-testid="stMarkdownContainer"],
body[data-theme="light"] [data-testid="stMetric"] {
    background-color: rgba(240, 240, 240, 0.95);
    color: #000000;
}

/* Modo oscuro: fondo negro, letras blancas */
body[data-theme="dark"] {
    background-color: #121212;
}
body[data-theme="dark"] [data-testid="stHeader"],
body[data-theme="dark"] [data-testid="stSidebar"],
body[data-theme="dark"] [data-testid="stMarkdownContainer"],
body[data-theme="dark"] [data-testid="stMetric"] {
    background-color: rgba(30, 30, 30, 0.85);
    color: #ffffff;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# =============================
# 3. ENTRADAS DEL USUARIO
# =============================
st.title("🔥 Calculadora Fitness 2.0")
st.markdown("Bienvenido a tu app de nutrición y entrenamiento. 💪")

st.header("📌 Datos personales")
nombre = st.text_input("Nombre completo")

col1, col2 = st.columns(2)
with col1:
    peso = st.number_input("Peso (kg)", min_value=30.0, max_value=200.0, step=0.1)
    altura = st.number_input("Altura (cm)", min_value=120.0, max_value=220.0, step=0.1)
with col2:
    edad = st.number_input("Edad (años)", min_value=10, max_value=100, step=1)
    sexo = st.selectbox("Sexo", ["Hombre", "Mujer"])

actividad = st.selectbox(
    "Nivel de actividad física",
    ["Sedentario", "Leve", "Moderada", "Intensa", "Muy intensa"]
)

objetivo = st.radio(
    "🎯 Objetivo",
    ["Mantener peso", "Bajar de peso", "Subir de peso"]
)

st.markdown("---")

# =============================
# 4. CÁLCULOS
# =============================
if sexo == "Hombre":
    tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
else:
    tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

factores = {
    "Sedentario": 1.2,
    "Leve": 1.375,
    "Moderada": 1.55,
    "Intensa": 1.725,
    "Muy intensa": 1.9
}
factor = factores[actividad]
gasto_diario = tmb * factor
imc = peso / ((altura/100) ** 2)

if objetivo == "Mantener peso":
    calorias_objetivo = gasto_diario
elif objetivo == "Bajar de peso":
    calorias_objetivo = gasto_diario - 500
else:
    calorias_objetivo = gasto_diario + 500

# =============================
# 5. RESULTADOS
# =============================
st.header("📊 Resultados")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("IMC", round(imc, 2))
with col2:
    st.metric("Tasa Metabólica Basal", f"{round(tmb)} kcal")
with col3:
    st.metric("Gasto Energético Diario", f"{round(gasto_diario)} kcal")

st.markdown("---")
st.subheader("✅ Recomendación")
if objetivo == "Mantener peso":
    st.success(f"Para mantener tu peso, deberías consumir alrededor de **{round(calorias_objetivo)} kcal** al día.")
elif objetivo == "Bajar de peso":
    st.warning(f"Para bajar de peso, deberías consumir aproximadamente **{round(calorias_objetivo)} kcal** al día.")
else:
    st.info(f"Para subir de peso, deberías consumir aproximadamente **{round(calorias_objetivo)} kcal** al día.")

st.caption("⚠️ Este cálculo es una estimación y no reemplaza la consulta con un nutricionista.")

# =============================
# 6. GUARDAR DATOS EN GOOGLE SHEETS
# =============================
if st.button("Guardar resultados"):
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datos = [fecha, nombre, edad, peso, altura, sexo, actividad, objetivo, round(calorias_objetivo)]
    sheet.append_row(datos)
    st.success("Tus datos fueron guardados en Google Sheets ✅")

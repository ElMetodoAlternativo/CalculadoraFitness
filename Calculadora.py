import streamlit as st

# --- FONDO FITNESS Y COLORES DE BLOQUES ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1599058917214-7d32d71b9a6b?fit=crop&w=1600&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Bloques que antes eran blancos (resultados en general) */
[data-testid="stMarkdownContainer"] {
    background-color: rgba(173, 216, 230, 0.85); /* azul claro semi-opaco */
    padding: 10px;
    border-radius: 10px;
}

/* Mantenemos otros bloques como títulos y métricas con sus colores anteriores */
[data-testid="stHeader"] {
    background-color: rgba(255, 255, 255, 0.95);
    padding: 10px;
    border-radius: 10px;
}

[data-testid="stMetric"] {
    background-color: rgba(200, 230, 201, 0.9); /* verde claro */
    padding: 10px;
    border-radius: 10px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)


# --- FONDO FITNESS ---
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.lovepik.com/bg/20231218/Expansive-Gym-Background-with-Abundance-of-Fitness-Equipment_2611111_wh1200.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Opcional: poner un color de fondo semi-transparente detrás de los textos para que se lean mejor */
[data-testid="stHeader"], [data-testid="stSidebar"], [data-testid="stMarkdownContainer"] {
    background-color: rgba(255, 255, 255, 0.90);
    padding: 10px;
    border-radius: 10px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

import streamlit as st

# --- TÍTULO PRINCIPAL ---
st.title("🔥 Calculadora de Calorías y Gasto Energético")
st.markdown("Bienvenido a tu app de nutrición personalizada. Completa los datos y obtén tu gasto energético estimado. 💪")

st.markdown("---")

# --- ENTRADAS DE USUARIO ---
st.header("📌 Datos personales")

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

# --- CÁLCULOS ---
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

# Ajuste según objetivo
if objetivo == "Mantener peso":
    calorias_objetivo = gasto_diario
elif objetivo == "Bajar de peso":
    calorias_objetivo = gasto_diario - 500  # déficit aproximado
else:  # Subir de peso
    calorias_objetivo = gasto_diario + 500  # superávit aproximado

# --- RESULTADOS ---
st.header("📊 Resultados")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("IMC", round(imc, 2))

with col2:
    st.metric("Tasa Metabólica Basal", f"{round(tmb)} kcal")

with col3:
    st.metric("Gasto Energético Diario", f"{round(gasto_diario)} kcal")

st.markdown("---")

# --- RECOMENDACIÓN ---
st.subheader("✅ Recomendación")
if objetivo == "Mantener peso":
    st.success(f"Para mantener tu peso, deberías consumir alrededor de **{round(calorias_objetivo)} kcal** al día.")
elif objetivo == "Bajar de peso":
    st.warning(f"Para bajar de peso, deberías consumir aproximadamente **{round(calorias_objetivo)} kcal** al día. Esto es un déficit de 500 kcal respecto a tu gasto.")
else:
    st.info(f"Para subir de peso, deberías consumir aproximadamente **{round(calorias_objetivo)} kcal** al día. Esto es un superávit de 500 kcal respecto a tu gasto.")

st.caption("⚠️ Este cálculo es una estimación y no reemplaza la consulta con un nutricionista.")


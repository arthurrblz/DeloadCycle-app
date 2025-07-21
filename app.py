
import streamlit as st
import datetime

# ========== CONFIGURAÇÕES DO APP ==========
st.set_page_config(page_title="DeloadCycle", page_icon="💪", layout="centered")

# ========== ESTILO PERSONALIZADO ==========
st.markdown("""
    <style>
        body {
            background-color: #0A0F2C;
        }
        .main {
            background-color: #0A0F2C;
        }
        .stApp {
            background-color: #0A0F2C;
        }
        h1, h2, h3, h4, h5, h6, .stText, .stLabel {
            color: #FFFFFF !important;
        }
        .stButton>button {
            background-color: #1A1F4C;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# ========== TÍTULO ==========
st.markdown("<h1 style='text-align: center;'>💪 DeloadCycle</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Seu planejador de treino com ciclos de deload</h4>", unsafe_allow_html=True)

# ========== SIDEBAR ==========
st.sidebar.image("icon.png", use_column_width=True)  # Ícone de braço fraco e forte com halter
st.sidebar.header("⚙️ Configurações")
total_semanas = st.sidebar.slider("Semanas antes do deload", 1, 12, 4)
inicio_treino = st.sidebar.date_input("📆 Início do ciclo", datetime.date.today())

# ========== CÁLCULO DE SEMANA ==========
hoje = datetime.date.today()
dias_passados = (hoje - inicio_treino).days
semana_atual = dias_passados // 7 + 1

# ========== STATUS DO CICLO ==========
st.subheader("📅 Semana atual do ciclo")

if semana_atual % total_semanas == 0:
    st.error(f"🛌 Semana {semana_atual} é uma **Semana de DELOAD!** Reduza cargas e volume.")
else:
    st.success(f"🏋️ Semana {semana_atual} de treino normal.")

# ========== FORMULÁRIO DE TREINO ==========
st.header("📋 Registrar treino")

with st.form("form_treino"):
    data = st.date_input("Data do treino", hoje)
    grupo = st.selectbox("Grupo muscular", [
        "Peito", "Costas", "Pernas", "Ombros", "Braços", "Abdômen", "Outros"
    ])
    exercicio = st.text_input("Exercício")
    series = st.number_input("Séries", min_value=1, max_value=10, value=3)
    reps = st.number_input("Repetições", min_value=1, max_value=30, value=10)
    carga = st.number_input("Carga (kg)", min_value=0.0, max_value=500.0, value=0.0)
    submit = st.form_submit_button("Salvar treino")

# ========== ARMAZENAR E MOSTRAR ==========
if "treinos" not in st.session_state:
    st.session_state.treinos = []

if submit:
    treino = {
        "data": str(data),
        "grupo": grupo,
        "exercicio": exercicio,
        "series": series,
        "reps": reps,
        "carga": carga
    }
    st.session_state.treinos.append(treino)
    st.success("✅ Treino salvo com sucesso!")

# ========== HISTÓRICO ==========
if st.session_state.treinos:
    st.header("📈 Histórico da sessão")
    for i, t in enumerate(reversed(st.session_state.treinos)):
        st.markdown(f"""
            - **{t['data']}** | *{t['grupo']}*: **{t['exercicio']}** — {t['series']}x{t['reps']} com {t['carga']}kg
        """)
else:
    st.info("Nenhum treino registrado ainda.")

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------

st.set_page_config(
    page_title="Dashboard Streamlit",
    page_icon="🚀",
    layout="wide"
)

# ------------------------------------------------
# SIDEBAR
# ------------------------------------------------

with st.sidebar:

    st.title("⚙️ Painel")

    nome = st.text_input(
        "Nome",
        value="Visitante"
    )

    categoria = st.selectbox(
        "Categoria",
        [
            "Vendas",
            "Financeiro",
            "Operações"
        ]
    )

    num_registros = st.slider(
        "Quantidade de linhas",
        10,
        500,
        100
    )

# ------------------------------------------------
# CABEÇALHO
# ------------------------------------------------

st.title("🚀 Dashboard Demonstrativo")

st.write(
    f"Bem-vindo **{nome}** | Categoria selecionada: **{categoria}**"
)

# ------------------------------------------------
# DADOS
# ------------------------------------------------

@st.cache_data
def gerar_dados(qtd):

    np.random.seed(42)

    return pd.DataFrame(
        {
            "Dia": pd.date_range(
                start="2024-01-01",
                periods=qtd
            ),
            "Vendas": np.random.randint(
                100,
                1000,
                qtd
            ),
            "Custos": np.random.randint(
                50,
                700,
                qtd
            )
        }
    )

df = gerar_dados(num_registros)

df["Lucro"] = df["Vendas"] - df["Custos"]

# ------------------------------------------------
# KPIs
# ------------------------------------------------

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "💰 Vendas Totais",
        f"R$ {df['Vendas'].sum():,.0f}"
    )

with col2:
    st.metric(
        "💸 Custos Totais",
        f"R$ {df['Custos'].sum():,.0f}"
    )

with col3:
    st.metric(
        "📈 Lucro",
        f"R$ {df['Lucro'].sum():,.0f}"
    )

# ------------------------------------------------
# TABS
# ------------------------------------------------

aba1, aba2, aba3 = st.tabs(
    [
        "📊 Gráficos",
        "📋 Dados",
        "📤 Upload"
    ]
)

# ------------------------------------------------
# ABA GRAFICOS
# ------------------------------------------------

with aba1:

    st.subheader("Vendas ao longo do tempo")

    fig = px.line(
        df,
        x="Dia",
        y="Vendas",
        markers=True,
        title="Evolução das Vendas"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Lucro")

    fig2 = px.bar(
        df,
        x="Dia",
        y="Lucro",
        color="Lucro",
        title="Lucro por Dia"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# ------------------------------------------------
# ABA DADOS
# ------------------------------------------------

with aba2:

    st.subheader("Tabela")

    st.dataframe(
        df,
        use_container_width=True
    )

    st.download_button(
        "⬇️ Baixar CSV",
        data=df.to_csv(index=False),
        file_name="dados.csv",
        mime="text/csv"
    )

# ------------------------------------------------
# ABA UPLOAD
# ------------------------------------------------

with aba3:

    arquivo = st.file_uploader(
        "Selecione um CSV",
        type=["csv"]
    )

    if arquivo:

        dados_usuario = pd.read_csv(
            arquivo
        )

        st.success("Arquivo carregado!")

        st.write(
            f"Linhas: {dados_usuario.shape[0]}"
        )

        st.dataframe(
            dados_usuario.head(),
            use_container_width=True
        )

# ------------------------------------------------
# EXPANDER
# ------------------------------------------------

with st.expander("ℹ️ Informações do Sistema"):

    st.write(
        {
            "Usuário": nome,
            "Categoria": categoria,
            "Data": datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            )
        }
    )

# ------------------------------------------------
# RODAPÉ
# ------------------------------------------------

st.markdown("---")

st.caption(
    "Google Colab + Streamlit + LocalTunnel"
)
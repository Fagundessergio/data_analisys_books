import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Análise Comparativa de Preços de Livros", page_icon="📚", layout="wide")

st.title("📈 Análise Comparativa de Preços de Livros")

DATA_DIR = r"D:\Programação\Desenvolvimento\Estudos Backend\Python\portifolio_analise_dados\data_analysis_books\dataset"
file_reviews = os.path.join(DATA_DIR, "customer reviews.csv")
file_books = os.path.join(DATA_DIR, "Top-100 Trending Books.csv")

if not os.path.exists(file_reviews) or not os.path.exists(file_books):
    st.error("❌ Um ou mais arquivos CSV não foram encontrados. Verifique os caminhos e tente novamente.")
    st.stop()

df_reviews = pd.read_csv(file_reviews)
df_books = pd.read_csv(file_books)

df_books.columns = df_books.columns.str.strip()

if "book price" not in df_books.columns:
    st.error("❌ A coluna 'book price' não foi encontrada no arquivo.")
    st.stop()

df_books["book price"] = pd.to_numeric(df_books["book price"], errors="coerce")
df_books.dropna(subset=["book price"], inplace=True)

price_min, price_max = df_books["book price"].min(), df_books["book price"].max()
min_year, max_year = int(df_books["year of publication"].min()), int(df_books["year of publication"].max())

st.sidebar.title("🔍 Filtros")
st.sidebar.info("Ajuste os parâmetros abaixo para refinar os resultados.")

price_range = st.sidebar.slider("💲 Intervalo de Preço", price_min, price_max, (price_min, price_max))
year_range = st.sidebar.slider("📅 Intervalo de Ano", min_year, max_year, (min_year, max_year))

with st.sidebar.expander(" Filtrar por Gênero", expanded=False):
    if "genre" in df_books.columns:
        all_genres = sorted(df_books["genre"].dropna().unique())
        selected_genres = st.multiselect("Selecione os gêneros:", all_genres, default=all_genres)
    else:
        selected_genres = None

sort_option = st.sidebar.selectbox(
    "Ordenar por", 
    ["Nenhum", "Preço Ascendente", "Preço Descendente", "Ano Ascendente", "Ano Descendente"]
)
df_filtered = df_books[
    (df_books["book price"] >= price_range[0]) &
    (df_books["book price"] <= price_range[1]) &
    (df_books["year of publication"] >= year_range[0]) &
    (df_books["year of publication"] <= year_range[1])
]
if selected_genres:
    df_filtered = df_filtered[df_filtered["genre"].isin(selected_genres)]
    
sort_dict = {
    "Preço Ascendente": ("book price", True),
    "Preço Descendente": ("book price", False),
    "Ano Ascendente": ("year of publication", True),
    "Ano Descendente": ("year of publication", False),
}
if sort_option in sort_dict:
    column, ascending = sort_dict[sort_option]
    df_filtered = df_filtered.sort_values(column, ascending=ascending)

st.sidebar.metric("📂 Número de Livros", len(df_filtered))
st.sidebar.metric("💵 Preço Médio", round(df_filtered["book price"].mean(), 2))
st.sidebar.metric("🟢 Preço Mínimo", round(df_filtered["book price"].min(), 2))
st.sidebar.metric("🔴 Preço Máximo", round(df_filtered["book price"].max(), 2))

if not df_filtered.empty:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style="background-color: #f0f0f5; padding: 20px; border-radius: 15px; 
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1); text-align: center;">
                <h3 style="color: #2a9d8f;"> Preço por Ano de Publicação</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.divider()
        fig_bar = px.bar(
            df_filtered, 
            x="year of publication", 
            y="book price",
            labels={"year of publication": "Ano de Publicação", "book price": "Preço (USD)"},
            color="book price",
            color_continuous_scale="viridis",
        )
        fig_bar.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", 
            margin=dict(l=50, r=50, t=30, b=50),
            font=dict(size=12, color='black'),
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        st.markdown(
            """
            <div style="background-color: #f0f0f5; padding: 20px; border-radius: 15px; 
            box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.1); text-align: center;">
                <h3 style="color: #ff7f0e;">Distribuição de Preços</h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.divider()
        fig_hist = px.histogram(
            df_filtered, x="book price", nbins=30,
            labels={"book price": "Preço (USD)"},
            color_discrete_sequence=["#ff7f0e"],
            opacity=0.8,
        )

        fig_hist.update_layout(
            plot_bgcolor="rgba(0,0,0,0)", 
            margin=dict(l=50, r=50, t=30, b=50),
            font=dict(size=12, color='black'),
        )

        st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown("### 📋 Livros Filtrados")
    st.dataframe(df_filtered, height=400)

else:
    st.warning("⚠️ Nenhum livro corresponde aos filtros selecionados.")

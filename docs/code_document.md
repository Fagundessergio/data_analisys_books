
# Documentação do Código

Este código é responsável por criar uma aplicação interativa de análise de dados sobre livros, utilizando o framework **Streamlit** para exibição das informações e gráficos. O objetivo é permitir a análise de preços de livros, juntamente com filtros e exibição de avaliações de livros.

## 1. **Configuração da Página Principal**

A primeira parte do código define a configuração da página principal, incluindo o título, o ícone da página e o layout.

```python
# Configuração da página
st.set_page_config(page_title="Análise Comparativa de Preços de Livros", page_icon="📚", layout="wide")
```

- **st.set_page_config**: Define o título da página, o ícone e o layout (largura total).

## 2. **Cabeçalho**

O cabeçalho da página é criado com o título do sistema:

```python
# Cabeçalho
st.title("📈 Análise Comparativa de Preços de Livros")
```

- **st.title**: Define o título principal da página.

## 3. **Carregamento de Dados**

O código faz o carregamento dos arquivos CSV com os dados de livros e avaliações. Ele também verifica se os arquivos existem no diretório especificado.

```python
# Definição dos caminhos dos arquivos
DATA_DIR = r"D:\Programação\Desenvolvimento\Estudos Backend\Python\portifolio_analise_dados\data_analysis_books\dataset"
file_reviews = os.path.join(DATA_DIR, "customer reviews.csv")
file_books = os.path.join(DATA_DIR, "Top-100 Trending Books.csv")

# Verificação da existência dos arquivos
if not os.path.exists(file_reviews) or not os.path.exists(file_books):
    st.error("❌ Um ou mais arquivos CSV não foram encontrados. Verifique os caminhos e tente novamente.")
    st.stop()
```

- **os.path.exists**: Verifica se os arquivos CSV existem no diretório.
- **st.error**: Exibe uma mensagem de erro caso os arquivos não sejam encontrados.

## 4. **Processamento dos Dados**

Após a verificação, os dados são carregados e processados. O código também normaliza as colunas e converte a coluna "book price" para valores numéricos.

```python
# Carregar os dados
df_reviews = pd.read_csv(file_reviews)
df_books = pd.read_csv(file_books)

# Normalizar os nomes das colunas
df_books.columns = df_books.columns.str.strip()

# Verificação da existência da coluna "book price"
if "book price" not in df_books.columns:
    st.error("❌ A coluna 'book price' não foi encontrada no arquivo.")
    st.stop()

# Converter colunas para os tipos corretos
df_books["book price"] = pd.to_numeric(df_books["book price"], errors="coerce")
df_books.dropna(subset=["book price"], inplace=True)
```

- **pd.read_csv**: Carrega os arquivos CSV para DataFrames do Pandas.
- **str.strip**: Remove espaços extras nos nomes das colunas.
- **pd.to_numeric**: Converte a coluna "book price" para valores numéricos.

## 5. **Cálculo de Preço e Ano Mínimo e Máximo**

Aqui, o código calcula os valores mínimos e máximos dos preços e anos de publicação dos livros.

```python
# Obter valores mínimo e máximo de preços e anos
price_min, price_max = df_books["book price"].min(), df_books["book price"].max()
min_year, max_year = int(df_books["year of publication"].min()), int(df_books["year of publication"].max())
```

- **min()** e **max()**: Calculam os valores mínimos e máximos para o preço dos livros e ano de publicação.

## 6. **Filtros e Sidebar**

A sidebar da aplicação contém filtros para o usuário selecionar o intervalo de preços, anos de publicação e gêneros de livros.

```python
# --- Sidebar (Filtros) ---
st.sidebar.title("🔍 Filtros")
st.sidebar.info("Ajuste os parâmetros abaixo para refinar os resultados.")
```

- **st.sidebar**: Exibe os filtros na barra lateral da interface.

### Filtro de Intervalo de Preço e Ano

```python
price_range = st.sidebar.slider("💲 Intervalo de Preço", price_min, price_max, (price_min, price_max))
year_range = st.sidebar.slider("📅 Intervalo de Ano", min_year, max_year, (min_year, max_year))
```

- **st.sidebar.slider**: Cria sliders para o intervalo de preços e anos.

### Filtro de Gênero

```python
with st.sidebar.expander(" Filtrar por Gênero", expanded=False):
    if "genre" in df_books.columns:
        all_genres = sorted(df_books["genre"].dropna().unique())
        selected_genres = st.multiselect("Selecione os gêneros:", all_genres, default=all_genres)
    else:
        selected_genres = None
```

- **st.sidebar.expander**: Cria uma seção expandível para o filtro de gênero.
- **st.multiselect**: Permite a seleção múltipla de gêneros.

### Ordenação

```python
sort_option = st.sidebar.selectbox(
    "Ordenar por", 
    ["Nenhum", "Preço Ascendente", "Preço Descendente", "Ano Ascendente", "Ano Descendente"]
)
```

- **st.sidebar.selectbox**: Cria uma caixa de seleção para ordenar os livros.

## 7. **Aplicação dos Filtros e Ordenação**

Depois de aplicar os filtros e ordenações, o DataFrame `df_filtered` é atualizado para exibir apenas os dados correspondentes.

```python
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
```

- **df_books[condition]**: Aplica filtros ao DataFrame.
- **sort_values**: Ordena os dados conforme a opção selecionada.

## 8. **Exibição de Métricas Rápidas e Gráficos**

O código exibe métricas rápidas sobre os livros filtrados e plota gráficos interativos utilizando Plotly.

```python
st.sidebar.metric("📂 Número de Livros", len(df_filtered))
st.sidebar.metric("💵 Preço Médio", round(df_filtered["book price"].mean(), 2))
st.sidebar.metric("🟢 Preço Mínimo", round(df_filtered["book price"].min(), 2))
st.sidebar.metric("🔴 Preço Máximo", round(df_filtered["book price"].max(), 2))
```

- **st.sidebar.metric**: Exibe métricas como número de livros, preço médio, mínimo e máximo.

### Gráficos de Preço por Ano e Distribuição de Preços

```python
fig_bar = px.bar(
    df_filtered, 
    x="year of publication", 
    y="book price",
    labels={"year of publication": "Ano de Publicação", "book price": "Preço (USD)"},
    color="book price",
    color_continuous_scale="viridis",
)
fig_hist = px.histogram(
    df_filtered, x="book price", nbins=30,
    labels={"book price": "Preço (USD)"},
    color_discrete_sequence=["#ff7f0e"],
    opacity=0.8,
)
```

- **px.bar** e **px.histogram**: Criam gráficos de barras e histogramas interativos.

## 9. **Exibição de Dados Filtrados**

Caso haja livros filtrados, eles são exibidos em uma tabela:

```python
st.dataframe(df_filtered, height=400)
```

- **st.dataframe**: Exibe o DataFrame com os livros filtrados em formato tabular.

## 10. **Exibição de Avaliações de Livros**

A segunda página exibe as avaliações dos livros selecionados. Ele carrega o CSV de avaliações e exibe as informações sobre o livro, incluindo a avaliação e o preço.

```python
df_reviews = pd.read_csv(r"D:\Programação\Desenvolvimento\Estudos Backend\Python\portifolio_analise_dados\data_analysis_books\dataset\customer reviews.csv")
```

- **st.sidebar.selectbox**: Permite selecionar o livro para exibir suas avaliações.
- **st.markdown**: Exibe as informações do livro de forma estilizada.

## Conclusão

Este código cria uma aplicação interativa de análise de dados utilizando Streamlit. Ele permite a visualização e análise de preços de livros, filtrando por preço, ano de publicação, gênero e outras opções, além de exibir avaliações de livros selecionados.

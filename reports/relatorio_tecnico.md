1. Visão Geral
O ENEM Insights é um projeto de Análise Exploratória de Dados (EDA) sobre os microdados do ENEM 2023, publicados pelo INEP. O objetivo é investigar desigualdades educacionais no Brasil cruzando o desempenho dos candidatos com fatores socioeconômicos e demográficos: renda familiar, tipo de escola, sexo, cor/raça e localização geográfica.
O projeto foi desenvolvido como peça de portfólio em Data Science, demonstrando o ciclo completo de um projeto de dados: coleta, limpeza, exploração, visualização e síntese de insights.

2. Problema e Perguntas de Negócio
As seguintes perguntas nortearam toda a análise:
Qual é o impacto da renda familiar no desempenho no ENEM?
Candidatos de escolas privadas têm vantagem em todas as áreas do conhecimento?
A vantagem da escola privada se mantém mesmo dentro da mesma faixa de renda?
Como o desempenho varia entre os 27 estados e 5 regiões do Brasil?
Existem diferenças de desempenho por sexo? Elas são uniformes entre as áreas?
Candidatos de diferentes grupos de cor/raça apresentam desempenhos distintos?
Quando múltiplos fatores desfavoráveis se somam, qual é o tamanho da desvantagem composta?

3. Dataset
Item
Detalhe
Fonte
INEP — Microdados do ENEM 2023
URL
gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem
Registros totais
3.933.955 candidatos
Amostra coletada
500.000 registros (amostragem aleatória)
Amostra limpa analisada
370.141 candidatos (após remoção de ausentes)
Registros removidos
~130.000 (26% da amostra) — candidatos ausentes em pelo menos uma prova
Formato original
CSV com separador ; e encoding latin-1
Formato processado
Parquet (via PyArrow)

Variáveis utilizadas:
Coluna original
Descrição
NU_NOTA_CN
Nota — Ciências da Natureza
NU_NOTA_CH
Nota — Ciências Humanas
NU_NOTA_LC
Nota — Linguagens e Códigos
NU_NOTA_MT
Nota — Matemática
NU_NOTA_REDACAO
Nota — Redação
Q006
Faixa de renda familiar (categorias A a P)
TP_ESCOLA
Tipo de escola (1=Não respondeu, 2=Pública, 3=Privada, 4=Exterior)
SG_UF_PROVA
Sigla do estado onde a prova foi realizada
TP_SEXO
Sexo do candidato (M/F)
TP_COR_RACA
Cor/raça autodeclarada (0–6)


4. Stack Tecnológica
Ferramenta
Versão
Uso
Python
3.11
Linguagem principal
Pandas
2.2.2
Manipulação e análise de dados
NumPy
1.26.4
Operações numéricas
Matplotlib
3.9.0
Visualizações estáticas
Seaborn
0.13.2
Gráficos estatísticos
Plotly
5.22.0
Mapa choropleth interativo
PyArrow
16.1.0
Leitura/escrita em Parquet
Requests
2.32.3
Download do GeoJSON do IBGE
Jupyter
1.0.0
Ambiente de desenvolvimento


5. Estrutura do Projeto
enem-insights/
├── data/
│   ├── raw/                          # Arquivo ZIP original (não versionado)
│   └── processed/                    # Parquet gerado após limpeza
├── notebooks/
│   ├── 01_carregamento_limpeza.ipynb
│   ├── 02_analise_univariada.ipynb
│   ├── 03_analise_bivariada.ipynb
│   ├── 03b_analise_geografica.ipynb
│   └── 04_insights_finais.ipynb
├── src/
│   └── utils.py                      # Mapeamentos, estilos e funções reutilizáveis
├── reports/
│   └── figures/                      # 21 gráficos exportados em PNG + 1 mapa HTML
├── .gitignore
├── requirements.txt
└── README.md



6. Metodologia — Notebooks
Notebook 01 — Carregamento e Limpeza
Objetivo: transformar o CSV bruto em um dataset limpo e eficiente para análise.
Etapas realizadas:
Leitura do arquivo ZIP diretamente via zipfile.ZipFile, sem descompactar no disco
Seleção das 10 colunas de interesse dentre as ~150 disponíveis nos microdados
Filtragem: remoção de candidatos com nota NaN em qualquer prova (ausentes/faltosos)
Aplicação de mapeamentos categóricos: renda (A–P → texto), escola (1–4 → texto), cor/raça (0–6 → texto), sexo (M/F → Masculino/Feminino)
Conversão de colunas categóricas para o dtype category do pandas (redução de memória)
Criação da coluna derivada NOTA_MEDIA (média aritmética das 5 notas)
Exportação para Parquet com PyArrow
Resultado: dataset limpo com 370.141 registros e 11 colunas, pronto para análise.

Notebook 02 — Análise Univariada
Objetivo: entender a distribuição individual de cada variável antes de cruzá-las.
Análises realizadas:
Histogramas + curva KDE para cada uma das 5 áreas de conhecimento
Boxplots comparativos entre as áreas
Gráficos de barras para distribuição de escola, sexo, cor/raça e faixa de renda
Ranking dos 27 estados por nota média (gráfico de barras horizontal)
Principais estatísticas descritivas:
Variável
Média
Mediana
Desvio Padrão
Nota Geral (média das 5 áreas)
541,6 pts
538,8 pts
—
Ciências da Natureza
~530 pts
—
—
Ciências Humanas
~550 pts
—
—
Linguagens e Códigos
~540 pts
—
—
Matemática
524,2 pts
510,1 pts
127,0 pts
Redação
647,5 pts
640,0 pts
—

Perfil demográfico da amostra:
Dimensão
Dado
Sexo
69,2% feminino (256.157) · 30,8% masculino (113.984)
Tipo de escola
54,3% não respondeu; entre quem respondeu: 87,3% pública · 12,7% privada
Cor/raça
Parda 44,4% · Branca 39,3% · Preta 13,2%
Renda
61,3% (226.843 candidatos) em faixas até R$ 1.980; faixa mais comum: "Até R$ 1.320" (36,9%)
Amplitude de estados
67,1 pts entre MG (572,7 pts) no topo e AM (505,6 pts) na base


Notebook 03 — Análise Bivariada
Objetivo: cruzar o desempenho com cada variável socioeconômica e demográfica para identificar padrões e medir a magnitude das desigualdades.
Análises realizadas:
Nota média por tipo de escola (barras com intervalo de confiança)
Nota média por faixa de renda — todas as 16 categorias
Heatmap nota média × renda × área de conhecimento
Nota por faixa de renda segmentada por tipo de escola (linha dupla)
Nota média por cor/raça (barras com desvio da média nacional)
Nota por área × sexo (comparação direta)
Principais achados:
#
Insight
Evidência quantitativa
1
Escola privada supera pública em todas as áreas
+163 pts em Redação · +130 pts em Matemática · +101 pts na média
2
Renda e desempenho têm relação monotônica crescente
+172 pts entre a faixa "Sem renda" e "Acima de R$ 39.600"
3
Desigualdade racial estrutural
Indígenas −82 pts vs brancos · Pretos −52 pts · Pardos −46 pts
4
Diferença por sexo é área-específica, não global
Homens +38 pts em Matemática · Mulheres +39 pts em Redação
5
Vantagem da escola privada independe da renda
Privada supera pública em todas as 16 faixas de renda — gap mínimo de 45 pts

O insight 5 é o mais relevante do notebook: demonstra que o tipo de escola tem um efeito próprio, separado do poder aquisitivo da família, sugerindo que o ambiente escolar, infraestrutura e qualidade do ensino explicam parte independente da diferença de desempenho.

Notebook 03b — Análise Geográfica
Objetivo: mapear a distribuição do desempenho pelos 27 estados e 5 regiões do Brasil, identificar padrões regionais e realizar um recorte específico sobre o Nordeste.
Análises realizadas:
Ranking dos 27 estados por nota média (barras coloridas por região)
Boxplot da distribuição de notas por região (Norte, Nordeste, Centro-Oeste, Sudeste, Sul)
Heatmap estado × área de conhecimento (27 linhas × 5 colunas)
Mapa choropleth interativo (Plotly) com escala de cores YlOrRd, zoom e hover com dados de cada estado
Recorte regional: comparação de Pernambuco com os demais estados do Nordeste e com a média nacional
Decisão técnica — mapa interativo:
O mapa foi construído com plotly.express.choropleth_mapbox usando o GeoJSON oficial do IBGE (API de malhas territoriais). O estilo mapbox_style='white-bg' foi escolhido por funcionar sem dependência de tiles externos, o que evitou problemas de renderização em ambientes offline e no VS Code. Scroll zoom foi habilitado via config={'scrollZoom': True}.
Principais achados — Geografia:
#
Insight
Evidência
1
Variação expressiva entre estados
67 pts entre MG (572,7) e AM (505,6)
2
Sul e Sudeste lideram com folga
Mediana ~557–561 pts vs Norte ~509 pts (+52 pts)
3
Matemática é a área com maior desigualdade regional
Amplitude de 87 pts: MG (565,7) vs AP (478,9)
4
DF se destaca dentro do Centro-Oeste
558,3 pts — 16,7 pts acima da média nacional

Recorte — Pernambuco no Nordeste:
PE é o 1º colocado no Nordeste com 539,8 pts
PE ocupa o 10º lugar no ranking nacional dos 27 estados
PE supera a média nordestina em todas as 5 áreas de conhecimento
Maior diferença em Matemática: +17,2 pts acima da média regional

Notebook 04 — Insights Finais
Objetivo: consolidar todos os achados anteriores em uma narrativa única, com visualizações síntese que colocam as diferentes dimensões de desigualdade em perspectiva comparada.
Análises realizadas:
1. Amplitude das Desigualdades (gráfico síntese)
Gráfico de barras horizontal que exibe, em uma única escala, o tamanho do gap de cada fator analisado:
Fator
Gap (pts)
Renda (sem renda → acima R$ 39k)
172
Tipo de escola (privada → pública)
101
Raça (branca → indígena)
82
Raça (branca → preta)
52
Região (Sul/Sudeste → Norte)
52
Raça (branca → parda)
46
Gênero — Redação (feminino → masculino)
39
Gênero — Matemática (masculino → feminino)
38

2. Desvantagem Composta
Comparação direta entre dois perfis extremos:
Perfil desfavorecido: escola pública · renda baixa ("Até R$ 1.320") · autodeclarado indígena
Perfil privilegiado: escola privada · renda alta ("Acima de R$ 39.600") · autodeclarado branco
Gap total entre os perfis: superior a 200 pontos — mais de 1,5 desvio padrão da distribuição geral.
Conclusão central: as desigualdades se acumulam. Cada fator desfavorável adiciona uma penalidade independente, e candidatos que concentram múltiplos fatores desfavoráveis partem de uma posição estruturalmente inferior — mais de dois desvios padrão abaixo dos grupos mais privilegiados.

7. Módulo Utilitário — src/utils.py
Arquivo Python com funções e constantes reutilizadas em todos os notebooks, evitando duplicação de código.
Constantes:
MAPA_RENDA — dicionário de tradução das categorias A–P para texto descritivo
MAPA_ESCOLA — mapeamento dos códigos 1–4 para tipo de escola
MAPA_COR_RACA — mapeamento dos códigos 0–6 para categorias de cor/raça
NOTAS_COLS — lista das 5 colunas de nota
NOTAS_LABELS — dicionário coluna → nome legível
PALETTE, FIGSIZE_DEFAULT — configurações visuais padrão
Funções:
Função
Descrição
configurar_estilo()
Aplica tema whitegrid (Seaborn) e remove bordas superior/direita dos eixos
salvar_figura(fig, nome, pasta)
Exporta figura Matplotlib em PNG para reports/figures/
nota_media(df)
Calcula média das 5 notas por candidato (ignora NaN)
formatar_eixo_mil(ax, eixo)
Formata eixo com separador de milhar no padrão PT-BR (ponto)


8. Visualizações Geradas
O projeto produziu 22 arquivos de saída em reports/figures/:
Notebook 02 — Análise Univariada:
02_histogramas_notas.png — Distribuição por área (histograma + KDE)
02_kde_comparativo.png — KDE das 5 áreas sobrepostas
02_boxplot_notas.png — Boxplot comparativo entre áreas
02_distribuicao_escola.png — Proporção por tipo de escola
02_distribuicao_sexo.png — Proporção por sexo
02_distribuicao_raca.png — Proporção por cor/raça
02_distribuicao_renda.png — Distribuição por faixa de renda
02_ranking_estados.png — Ranking dos 27 estados por nota média
Notebook 03 — Análise Bivariada:
03_nota_por_escola.png — Nota média por tipo de escola
03_nota_por_renda.png — Nota média por faixa de renda
03_heatmap_renda_area.png — Heatmap renda × área de conhecimento
03_nota_renda_por_escola.png — Nota por renda segmentada por escola
03_nota_por_raca.png — Nota por cor/raça
03_notas_por_sexo.png — Nota por área × sexo
Notebook 03b — Análise Geográfica:
03b_ranking_estados.png — Ranking colorido por região
03b_nota_por_regiao.png — Boxplot regional
03b_heatmap_uf_area.png — Heatmap estado × área
03b_recorte_nordeste_pe.png — Comparativo PE vs demais estados do Nordeste
03b_mapa_interativo.html — Mapa choropleth interativo (Plotly)
Notebook 04 — Insights Finais:
04_mapa_desigualdades.png — Amplitude dos gaps por fator
04_desvantagem_composta.png — Comparação dos perfis extremos

9. Decisões Técnicas Relevantes
Amostragem: Com 3,9 milhões de registros, o dataset completo seria pesado para EDA exploratória. Uma amostra aleatória de 500k registros (12,7% do total) foi suficiente para obter estimativas estáveis das métricas investigadas.
Formato Parquet: após a limpeza no notebook 01, o dataset é salvo em Parquet. Isso reduz o tempo de carregamento nos notebooks seguintes e mantém os tipos de coluna (inclusive category) sem necessidade de reprocessamento.
Mapa interativo sem tiles externos: px.choropleth_mapbox com mapbox_style='white-bg' funciona sem requisitar CDN externo, o que garante renderização consistente em qualquer ambiente (VS Code, JupyterLab, CI). Alternativas como carto-positron falhavam silenciosamente em redes restritas.
Média nacional ponderada vs. média de médias estaduais: ao calcular a média nacional para comparação no recorte do Nordeste, foi usada df['NOTA_MEDIA'].mean() (541,6 pts) e não nota_uf['nota_media'].mean() (536,6 pts). A segunda é uma média não ponderada das médias estaduais, enviesada por estados com poucos candidatos, e não representa a média real do país.
Vantagem da escola privada independente da renda (insight mais forte): a análise de interação renda × escola demonstra que, mesmo quando se controla pela renda familiar, candidatos de escola privada consistentemente superam os de escola pública em todas as 16 faixas — com o gap mínimo de 45 pts na faixa de renda mais baixa. Isso indica que o tipo de escola tem poder explicativo próprio, além do efeito da renda.

10. Histórico de Commits
Hash
Mensagem
430a5c4
Initial commit
7dcb9c3
feat: estrutura do projeto e notebook de carregamento/limpeza
4af7977
feat: notebooks 01 e 02 com dados ENEM 2023 + README profissional
d38bb5c
feat: notebook 03 de analise bivariada com insights reais
5f672bf
feat: notebook 03b de análise geográfica com mapa choropleth interativo
628a841
chore: atualiza metadados de execução do notebook 03
15dbf8d
fix: corrige inconsistências encontradas na revisão do projeto
c557b18
docs: preenche observações com valores reais e atualiza README
dc6ed6d
feat: notebook 04 de insights finais com gráficos síntese
9aad69d
fix: corrige ano do ENEM de 2024 para 2023 nos títulos do notebook 02
3a2457f
docs: adiciona docstrings Google Style em todas as funções de utils.py
708bf87
docs: adiciona LinkedIn na seção Autor do README
102ebca
fix: adiciona regras globais para *.zip e *.csv no .gitignore
96d96fd
feat: adiciona seção de recorte regional Nordeste/PE no notebook 03b
7578242
fix: corrige media_nacional na seção PE/Nordeste e atualiza README
6c06e1f
chore: atualiza outputs de execução (EOL e mapa HTML regenerado)


11. Como Reproduzir
# 1. Clone o repositório
git clone https://github.com/Rodrigotorres1/enem-insights.git
cd enem-insights

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Baixe os microdados do ENEM 2023 no portal do INEP
#    e coloque o arquivo ZIP em data/raw/

# 4. Execute os notebooks em ordem
jupyter notebook notebooks/


Requisito mínimo: Python 3.11+

12. Limitações e Possíveis Extensões
Limitações:
A análise é descritiva (EDA), não causal. Correlações identificadas não estabelecem causalidade.
A amostra de 500k exclui 87% do dataset; padrões de grupos menores (ex: indígenas, candidatos do exterior) podem ser subestimados.
A variável TP_ESCOLA tem 54,3% de "Não respondeu", limitando a análise de tipo de escola.
Sem dados de anos anteriores, não é possível identificar tendências temporais.
Possíveis extensões:
Análise temporal: comparar os dados de 2019 a 2023 para observar impacto da pandemia
Modelagem preditiva: regressão ou gradient boosting para prever nota a partir das variáveis socioeconômicas
Análise municipal: os microdados incluem município de residência, permitindo granularidade além do estado
Dashboard interativo: transformar os insights em um painel Streamlit ou Dash para apresentação

# PIB Nominal: G7 vs BRICS (1970–presente)

Pipeline de preparação de dados que transforma a série histórica de PIB nominal do Banco Mundial em um dataset pronto para visualização em corrida de barras (bar chart race) no Flourish.

## Objetivo

Comparar a evolução do PIB nominal (em US\$ trilhões) dos países do **G7** e dos **BRICS** ao longo do tempo, permitindo visualizar a mudança de peso econômico entre os dois blocos.

## Fonte dos dados

- **World Bank Open Data** — indicador [GDP (current US\$)](https://data.worldbank.org/indicator/NY.GDP.MKTP.CD)
- Arquivo baixado diretamente do site do Banco Mundial em formato CSV (`gdp_nominal.csv`), incluindo os metadados padrão que o World Bank adiciona nas primeiras linhas do arquivo.

## O que os scripts fazem

Há duas versões do mesmo pipeline — uma em português (`gerar_gdp_flourish.py`) e uma em inglês (`gerar_gdp_english.py`), usadas respectivamente para o público brasileiro e para o canal internacional. A lógica é idêntica; muda apenas o idioma dos rótulos gerados no CSV final.

Cada script recebe o CSV bruto do World Bank e devolve um CSV já formatado para o Flourish, com:

1. **Filtragem dos países-alvo**: os 7 membros do G7 e os 9 membros atuais dos BRICS (incluindo a expansão de 2024 — Egito, Etiópia, Irã e Emirados Árabes Unidos).
2. **Seleção do período**: apenas dados a partir de 1970.
3. **Conversão de escala**: os valores brutos do World Bank vêm em dólares "crus" (ex: `25000000000000`); o script converte tudo para **trilhões de US\$**, formato muito mais legível em um gráfico.
4. **Preenchimento de lacunas**: alguns países têm anos sem dado reportado. Uso interpolação linear (`pandas.interpolate`) para preencher pequenas lacunas *dentro* da série histórica de cada país — sem, no entanto, criar valores para anos anteriores ao primeiro dado real disponível (ex: a Rússia como "Russian Federation" só existe como entidade a partir de 1991/92).
5. **Enriquecimento visual**: adiciona a bandeira de cada país (via [flagcdn.com](https://flagcdn.com)) e a categoria do bloco (G7 ou BRICS), campos que o Flourish usa para colorir e rotular as barras.

## 🗂️ Estrutura

```
📁 gdp-g7-brics-race/
├── README.md
├── gerar_gdp_flourish.py              # script de preparação — versão em português
├── gerar_gdp_english.py               # script de preparação — versão em inglês
├── flourish_gdp_brics_vs_g7.csv       # saída processada (PT), pronta para o Flourish
└── flourish_gdp_brics_vs_g7_en.csv    # saída processada (EN), pronta para o Flourish
```

## Como rodar

```bash
pip install pandas

# versão em português
python gerar_gdp_flourish.py

# versão em inglês
python gerar_gdp_english.py
```

Cada script gera seu respectivo CSV, que pode ser importado diretamente em um template de **Bar Chart Race** no [Flourish Studio](https://flourish.studio/).

## Principais decisões técnicas

- **Por que interpolar em vez de deixar em branco?** Uma corrida de barras "quebra" visualmente quando um país some e reaparece. A interpolação linear suaviza pequenas falhas pontuais de reporte sem inventar tendência — só preenche o intervalo entre dois pontos reais já existentes.
- **Por que converter para trilhões?** Os valores brutos do World Bank têm 13-14 dígitos, o que atrapalha a leitura dos rótulos no gráfico. Trilhões de dólares é a escala mais legível para comparação entre as maiores economias do mundo.
- **Por que Flourish e não só Python/Matplotlib?** O Flourish tem um template pronto e bem otimizado para bar chart race (interpolação de frames entre anos, transições suaves), o que economiza bastante tempo de desenvolvimento comparado a recriar a animação do zero.

## Resultado

- Visualização publicada no Flourish: *[[link aqui](https://public.flourish.studio/visualisation/29835010/)]*

## 🛠️ Tecnologias

- Python (pandas)
- Flourish Studio (visualização)

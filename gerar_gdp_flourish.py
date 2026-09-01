import pandas as pd

# 1. Carrega o arquivo do Banco Mundial (pula as 4 linhas de metadados do cabeçalho)
try:
    df = pd.read_csv('gdp_nominal.csv', skiprows=4)
except Exception:
    df = pd.read_csv('gdp_nominal.csv')

# 2. Define os blocos
g7_paises = ['United States', 'United Kingdom', 'Germany', 'France', 'Italy', 'Japan', 'Canada']
brics_paises = ['Brazil', 'Russian Federation', 'India', 'China', 'South Africa', 'Egypt, Arab Rep.', 'Ethiopia', 'Iran, Islamic Rep.', 'United Arab Emirates']

# Mapeamento para nomes padronizados e URLs das bandeiras ISO
mapeamento_paises = {
    'United States': ('EUA (G7)', 'us', 'G7'),
    'United Kingdom': ('Reino Unido (G7)', 'gb', 'G7'),
    'Germany': ('Alemanha (G7)', 'de', 'G7'),
    'France': ('França (G7)', 'fr', 'G7'),
    'Italy': ('Itália (G7)', 'it', 'G7'),
    'Japan': ('Japão (G7)', 'jp', 'G7'),
    'Canada': ('Canadá (G7)', 'ca', 'G7'),
    'Brazil': ('Brasil (BRICS)', 'br', 'BRICS'),
    'Russian Federation': ('Rússia (BRICS)', 'ru', 'BRICS'),
    'India': ('Índia (BRICS)', 'in', 'BRICS'),
    'China': ('China (BRICS)', 'cn', 'BRICS'),
    'South Africa': ('África do Sul (BRICS)', 'za', 'BRICS'),
    'Egypt, Arab Rep.': ('Egito (BRICS)', 'eg', 'BRICS'),
    'Ethiopia': ('Etiópia (BRICS)', 'et', 'BRICS'),
    'Iran, Islamic Rep.': ('Irã (BRICS)', 'ir', 'BRICS'),
    'United Arab Emirates': ('EAU (BRICS)', 'ae', 'BRICS')
}

# 3. Filtra apenas os países dos dois blocos
df_filtrado = df[df['Country Name'].isin(mapeamento_paises.keys())].copy()

# 4. Seleciona os anos de 1970 até o mais recente
colunas_anos = [col for col in df_filtrado.columns if col.isdigit() and int(col) >= 1970]

# 5. Organiza a tabela para o Flourish
df_flourish = df_filtrado.set_index('Country Name')[colunas_anos]

# Converter para Trilhões de Dólares (facilita a leitura e evita números com 12 zeros)
df_flourish = df_flourish.astype(float) / 1e12

# Preenche pequenas lacunas com interpolação linear
df_flourish = df_flourish.interpolate(axis=1, method='linear')

# 6. Adiciona Nomes Formatados, Bandeiras e Categorias
nomes_formatados = [mapeamento_paises[c][0] for c in df_flourish.index]
bandeiras = [f"https://flagcdn.com/w80/{mapeamento_paises[c][1]}.png" for c in df_flourish.index]
categorias = [mapeamento_paises[c][2] for c in df_flourish.index]

df_flourish.index = nomes_formatados
df_flourish.insert(0, 'Image', bandeiras)
df_flourish.insert(1, 'Category', categorias)
df_flourish.index.name = 'Country'

# 7. Salva o CSV final
df_flourish.to_csv('flourish_gdp_brics_vs_g7.csv')

print("Arquivo 'flourish_gdp_brics_vs_g7.csv' gerado com sucesso!")
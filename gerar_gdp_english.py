import pandas as pd

# 1. Load the World Bank CSV (skipping metadata header rows)
try:
    df = pd.read_csv('gdp_nominal.csv', skiprows=4)
except Exception:
    df = pd.read_csv('gdp_nominal.csv')

# 2. Define standard mapping for G7 and BRICS countries
# Format: 'Original World Bank Name': ('Display Name in English', 'ISO flag code', 'Bloc Category')
country_mapping = {
    # G7 Members
    'United States': ('United States (G7)', 'us', 'G7'),
    'United Kingdom': ('United Kingdom (G7)', 'gb', 'G7'),
    'Germany': ('Germany (G7)', 'de', 'G7'),
    'France': ('France (G7)', 'fr', 'G7'),
    'Italy': ('Italy (G7)', 'it', 'G7'),
    'Japan': ('Japan (G7)', 'jp', 'G7'),
    'Canada': ('Canada (G7)', 'ca', 'G7'),
    
    # BRICS Members (Expanded)
    'Brazil': ('Brazil (BRICS)', 'br', 'BRICS'),
    'Russian Federation': ('Russia (BRICS)', 'ru', 'BRICS'),
    'India': ('India (BRICS)', 'in', 'BRICS'),
    'China': ('China (BRICS)', 'cn', 'BRICS'),
    'South Africa': ('South Africa (BRICS)', 'za', 'BRICS'),
    'Egypt, Arab Rep.': ('Egypt (BRICS)', 'eg', 'BRICS'),
    'Ethiopia': ('Ethiopia (BRICS)', 'et', 'BRICS'),
    'Iran, Islamic Rep.': ('Iran (BRICS)', 'ir', 'BRICS'),
    'United Arab Emirates': ('UAE (BRICS)', 'ae', 'BRICS')
}

# 3. Filter only the target countries
df_filtered = df[df['Country Name'].isin(country_mapping.keys())].copy()

# 4. Select year columns from 1970 onwards
year_columns = [col for col in df_filtered.columns if col.isdigit() and int(col) >= 1970]

# 5. Structure dataset for Flourish
df_flourish = df_filtered.set_index('Country Name')[year_columns]

# Convert values to Trillions of USD (e.g. $25,000,000,000,000 becomes 25.0)
df_flourish = df_flourish.astype(float) / 1e12

# Fill any small gaps with linear interpolation
df_flourish = df_flourish.interpolate(axis=1, method='linear')

# 6. Insert English Labels, Flags, and Categories
display_names = [country_mapping[c][0] for c in df_flourish.index]
flags = [f"https://flagcdn.com/w80/{country_mapping[c][1]}.png" for c in df_flourish.index]
categories = [country_mapping[c][2] for c in df_flourish.index]

df_flourish.index = display_names
df_flourish.insert(0, 'Image', flags)
df_flourish.insert(1, 'Category', categories)
df_flourish.index.name = 'Country'

# 7. Save the final CSV
df_flourish.to_csv('flourish_gdp_brics_vs_g7_en.csv')

print("File 'flourish_gdp_brics_vs_g7_en.csv' successfully generated in English!")
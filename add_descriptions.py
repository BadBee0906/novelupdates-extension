import cloudscraper
from bs4 import BeautifulSoup
import pandas as pd
import random
import time
import sys
import csv

# Configuración de user-agents para rotación
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66'
]

# Cargar CSV
df = pd.read_csv('novel_data.csv')
if 'description' not in df.columns:
    df['description'] = ''

# Forzar tipo object para evitar warnings y permitir strings
df['description'] = df['description'].astype(object)

# Crear slugs si no existen
if 'slug' not in df.columns:
    df['slug'] = df['name'].str.lower().str.replace(' ', '-').str.replace(r'[^a-z0-9-]', '', regex=True)

# Limita a 20 novelas para pruebas (ajusta según necesidad)
slugs = df['slug'].head(200).tolist()
random.shuffle(slugs)

# Inicializar cloudscraper
scraper = cloudscraper.create_scraper(
    interpreter="nodejs",
    browser={
        "browser": "chrome",
        "platform": "ios",
        "desktop": False,
    }
)

for slug in slugs:
    # Obtener valor actual y convertir a string seguro
    current_desc = df.loc[df['slug'] == slug, 'description'].values[0]
    current_desc = str(current_desc) if pd.notna(current_desc) else ''

    if current_desc.strip() != '':
        print(f"Descripción ya existe para {slug}, saltando...")
        continue

    url = f"https://www.novelupdates.com/series/{slug}/"
    try:
        headers = {'User-Agent': random.choice(user_agents)}
        response = scraper.get(url, headers=headers, timeout=30)

        # Detectar bloqueos de Cloudflare
        if any(code in response.text for code in ["403 Forbidden", "429 Too Many Requests", "Access denied", "Cloudflare"]):
            print(f"⚠️ Bloqueo Cloudflare detectado en {slug}. Deteniendo script.")
            df.to_csv('novel_data.csv', index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)
            sys.exit(1)

        soup = BeautifulSoup(response.text, 'html.parser')
        desc_div = soup.find('div', id='editdescription')
        description = desc_div.text.strip() if desc_div else ''
        df.loc[df['slug'] == slug, 'description'] = description
        print(f"✅ Descripción añadida para {slug}")

        # Delay aleatorio entre 5-15 segundos
        time.sleep(random.uniform(5, 15))

    except Exception as e:
        print(f"❌ Error en {slug}: {e}")
        # Detener si es 403/429
        if '403' in str(e) or '429' in str(e):
            print("🚫 Posible detección. Deteniendo script.")
            df.to_csv('novel_data.csv', index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)
            sys.exit(1)

# Guardar CSV actualizado con soporte Unicode seguro
df.to_csv('novel_data.csv', index=False, encoding='utf-8-sig', quoting=csv.QUOTE_ALL)
print("✅ CSV actualizado con descripciones (Unicode seguro).")

import pandas as pd

# Cargar el nuevo dataset
df = pd.read_csv('novel_data.csv')

# Mostrar columnas
print("Columnas del nuevo dataset:")
print(df.columns.tolist())

# Mostrar primeras 5 filas
print("\nPrimeras 5 filas:")
print(df.head())

# Información general (tipos de datos, nulos)
print("\nInformación general:")
print(df.info())

# Contar nulos por columna
print("\nValores nulos por columna:")
print(df.isnull().sum())

# Ejemplos de géneros y tags (para verificar formato)
print("\nEjemplos de géneros (primeras 5):")
print(df['genres'].head())
print("\nEjemplos de tags (primeras 5):")
print(df['tags'].head())

# Verificar columnas clave para el backend
required_columns = ['id', 'name', 'genres', 'tags', 'rating', 'activity_all_time_rank']
missing = [col for col in required_columns if col not in df.columns]
if missing:
    print(f"\nColumnas faltantes: {missing}")
else:
    print("\nTodas las columnas clave están presentes.")
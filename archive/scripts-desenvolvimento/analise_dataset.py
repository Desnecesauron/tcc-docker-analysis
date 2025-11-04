import pandas as pd
import sys

# Verifica se um caminho de arquivo foi passado como argumento
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    file_path = 'data/spam_ptbr_v3.tsv'

# Carrega o dataset
try:
    df = pd.read_csv(file_path, sep='\t', on_bad_lines='skip')
except FileNotFoundError:
    print(f"Erro: Arquivo não encontrado em '{file_path}'")
    sys.exit(1)

print(f"--- Análise do Dataset {file_path} ---")

# 1. Tamanho do Dataset
print(f"\n1. Tamanho Total do Dataset: {len(df)} mensagens")

# 2. Balanceamento de Classes
print("\n2. Balanceamento de Classes:")
print(df['label'].value_counts())

# 3. Mensagens Duplicadas
num_duplicates = df.duplicated().sum()
print(f"\n3. Total de Mensagens Duplicadas: {num_duplicates}")

# 4. Amostra de Mensagens de Spam Duplicadas
spam_duplicates = df[df['label'] == 'spam'][df[df['label'] == 'spam'].duplicated(keep=False)].sort_values(by='message')

print("\n4. Amostra de Mensagens de Spam Duplicadas (e sua frequência):")
print(spam_duplicates['message'].value_counts().head(10))

# 5. Amostra de Mensagens de Ham Duplicadas
ham_duplicates = df[df['label'] == 'ham'][df[df['label'] == 'ham'].duplicated(keep=False)].sort_values(by='message')

print("\n5. Amostra de Mensagens de Ham Duplicadas (e sua frequência):")
print(ham_duplicates['message'].value_counts().head(10))


print("\n--- Fim da Análise ---")
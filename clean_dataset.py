import pandas as pd

# Carrega o dataset
df = pd.read_csv('data/spam_ptbr.tsv', sep='\t')

# Remove duplicatas
df.drop_duplicates(subset='message', inplace=True)

# Salva o novo dataset
df.to_csv('data/spam_ptbr_v2.tsv', sep='\t', index=False)

print("Dataset limpo e salvo em data/spam_ptbr_v2.tsv")

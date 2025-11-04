import pandas as pd
import sys
import matplotlib.pyplot as plt

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

# Calcula o comprimento de cada mensagem
df['length'] = df['message'].str.len()

# Separa o dataset em spam e ham
spam_df = df[df['label'] == 'spam']
ham_df = df[df['label'] == 'ham']

# Plota a distribuição do comprimento das mensagens
plt.figure(figsize=(12, 6))
plt.hist(spam_df['length'], bins=50, alpha=0.5, label='Spam', color='red')
plt.hist(ham_df['length'], bins=50, alpha=0.5, label='Ham', color='blue')
plt.title('Distribuição do Comprimento das Mensagens')
plt.xlabel('Comprimento da Mensagem')
plt.ylabel('Frequência')
plt.legend(loc='upper right')
plt.savefig('length_distribution.png')

print("Análise de comprimento concluída. Gráfico salvo como 'length_distribution.png'")

# Imprime estatísticas descritivas do comprimento das mensagens
print("\nEstatísticas do Comprimento das Mensagens de Spam:")
print(spam_df['length'].describe())

print("\nEstatísticas do Comprimento das Mensagens de Ham:")
print(ham_df['length'].describe())

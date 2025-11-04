
import pandas as pd

# Load the existing dataset
df = pd.read_csv('data/spam_ptbr_v3.tsv', sep='	')

# List of new ham messages
new_ham_messages = [
    "oi", "tudo bem?", "bom dia", "boa tarde", "boa noite", "obrigado", "de nada", "por favor",
    "com licença", "desculpe", "sim", "não", "talvez", "até logo", "até amanhã", "tchau",
    "legal", "que bom", "pois é", "verdade", "sei", "entendi", "não sei", "não entendi",
    "como assim?", "por quê?", "onde?", "quando?", "quem?", "o que?", "é bom", "é ruim",
    "gostei", "não gostei", "quero", "não quero", "preciso", "não preciso", "vamos", "agora",
    "depois", "hoje", "amanhã", "ontem", "sempre", "nunca", "talvez", "com certeza", "claro",
    "óbvio", "pode ser", "tá", "ok", "beleza", "fechado", "combinado", "já volto", "estou aqui",
    "estou ocupado", "estou livre", "te ligo mais tarde", "me liga", "que horas?", "onde vamos?",
    "o que vamos fazer?", "estou com fome", "estou com sede", "estou cansado", "estou doente",
    "estou feliz", "estou triste", "parabéns", "feliz aniversário", "feliz natal", "feliz ano novo",
    "sinto muito", "meus pêsames", "boa sorte", "bom trabalho", "continue assim", "força",
    "coragem", "calma", "relaxa", "deixa pra lá", "esquece", "não se preocupe",
    "vai dar tudo certo", "confia em mim", "acredite", "duvido", "impossível", "improvável",
    "provavelmente", "quem sabe", "depende", "tanto faz", "qualquer um", "qualquer coisa",
    "nada", "tudo", "ninguém", "todo mundo"
]

# Create a new DataFrame for the new messages
new_df = pd.DataFrame({
    'label': 'ham',
    'message': new_ham_messages
})

# Concatenate the old and new DataFrames
df_augmented = pd.concat([df, new_df], ignore_index=True)

# Remove duplicates
df_augmented.drop_duplicates(subset='message', inplace=True)

# Save the augmented dataset
df_augmented.to_csv('data/spam_ptbr_v4.tsv', sep='	', index=False)

print('Dataset augmented and saved to data/spam_ptbr_v4.tsv')

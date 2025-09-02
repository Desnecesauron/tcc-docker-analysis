import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os
import nltk
from nltk.corpus import stopwords

# --- MODIFICAÇÃO 1: Baixar a lista de stop words em português ---
try:
    stopwords.words('portuguese')
except LookupError:
    print("Baixando recursos do NLTK (stopwords)...")
    nltk.download('stopwords')

# --- Carregamento e Preparação dos Dados ---

# --- MODIFICAÇÃO 2: Ler o novo arquivo CSV em português ---
# Usamos encoding='utf-8' para garantir a leitura de caracteres especiais (ç, ã, etc.)
# df = pd.read_csv('data/spam_ptbr.csv', encoding='utf-8')
df = pd.read_csv('data/spam_ptbr.tsv', encoding='latin-1', sep='\t')
print("Dataset em português carregado.")
# O resto do pré-processamento continua igual, pois o CSV tem os mesmos nomes de coluna.
df['label'] = df['label'].map({'ham': 0, 'spam': 1})
df.dropna(inplace=True)

# --- Treinamento do Modelo ---
X = df['message']
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- MODIFICAÇÃO 3: Usar stop words em português no vetorizador ---
portuguese_stopwords = stopwords.words('portuguese')
vectorizer = TfidfVectorizer(stop_words=portuguese_stopwords, max_features=5000)

X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# O treinamento do modelo não muda
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)
print("Modelo treinado com dados em Português do Brasil.")

# --- Avaliação e Salvamento (sem alterações) ---
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acurácia do modelo no conjunto de teste: {accuracy:.4f}")

if not os.path.exists('models'):
    os.makedirs('models')

joblib.dump(model, 'models/model.pkl')
joblib.dump(vectorizer, 'models/vectorizer.pkl')

print("Modelo e vetorizador PT-BR salvos em 'models/'.")

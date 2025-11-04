import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import FunctionTransformer
import joblib
import os
import nltk
from nltk.corpus import stopwords
import re

# Importar TODAS as features (originais + avançadas + impersonation)
from features import (
    # Features originais
    has_url, has_phone_number, has_money_keywords, has_urgency_keywords,
    # Features avançadas de URL
    num_urls, has_ip_url, has_shortened_url, avg_url_length,
    has_suspicious_tld, max_subdomain_depth, has_encoded_chars,
    # Features de phishing específicas
    has_at_in_url, max_hyphens_in_domain, has_numbers_in_domain,
    has_nonstandard_port, url_entropy,
    # Features de impersonation e engenharia social
    has_institution_name, has_data_request, has_prize_claim,
    has_threat_language, has_large_money_amount, has_action_required
)

# --- MODIFICAÇÃO 1: Baixar a lista de stop words em português ---
try:
    stopwords.words('portuguese')
except LookupError:
    print("Baixando recursos do NLTK (stopwords)...")
    nltk.download('stopwords')

# --- Carregamento e Preparação dos Dados ---
df = pd.read_csv('data/spam_ptbr_v5.tsv', encoding='utf-8', sep='\t', on_bad_lines='skip')
print("Dataset em português carregado (v5 - com impersonation scams).")
df['label'] = df['label'].map({'ham': 0, 'spam': 1})
df.dropna(inplace=True)

# --- Treinamento do Modelo ---
X = df[['message']]
y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- MODIFICAÇÃO 3: Usar stop words em português no vetorizador ---
portuguese_stopwords = stopwords.words('portuguese')

# --- Create a ColumnTransformer to combine features ---
preprocessor = ColumnTransformer(
    transformers=[
        # TF-IDF Vectorizer (texto)
        ('tfidf', TfidfVectorizer(stop_words=portuguese_stopwords, max_features=10000, ngram_range=(1, 3)), 'message'),

        # Features originais
        ('has_url', FunctionTransformer(has_url, validate=False), 'message'),
        ('has_phone_number', FunctionTransformer(has_phone_number, validate=False), 'message'),
        ('has_money_keywords', FunctionTransformer(has_money_keywords, validate=False), 'message'),
        ('has_urgency_keywords', FunctionTransformer(has_urgency_keywords, validate=False), 'message'),

        # Features avançadas de URL
        ('num_urls', FunctionTransformer(num_urls, validate=False), 'message'),
        ('has_ip_url', FunctionTransformer(has_ip_url, validate=False), 'message'),
        ('has_shortened_url', FunctionTransformer(has_shortened_url, validate=False), 'message'),
        ('avg_url_length', FunctionTransformer(avg_url_length, validate=False), 'message'),
        ('has_suspicious_tld', FunctionTransformer(has_suspicious_tld, validate=False), 'message'),
        ('max_subdomain_depth', FunctionTransformer(max_subdomain_depth, validate=False), 'message'),
        ('has_encoded_chars', FunctionTransformer(has_encoded_chars, validate=False), 'message'),

        # Features de phishing específicas
        ('has_at_in_url', FunctionTransformer(has_at_in_url, validate=False), 'message'),
        ('max_hyphens_in_domain', FunctionTransformer(max_hyphens_in_domain, validate=False), 'message'),
        ('has_numbers_in_domain', FunctionTransformer(has_numbers_in_domain, validate=False), 'message'),
        ('has_nonstandard_port', FunctionTransformer(has_nonstandard_port, validate=False), 'message'),
        ('url_entropy', FunctionTransformer(url_entropy, validate=False), 'message'),

        # Features de impersonation e engenharia social
        ('has_institution_name', FunctionTransformer(has_institution_name, validate=False), 'message'),
        ('has_data_request', FunctionTransformer(has_data_request, validate=False), 'message'),
        ('has_prize_claim', FunctionTransformer(has_prize_claim, validate=False), 'message'),
        ('has_threat_language', FunctionTransformer(has_threat_language, validate=False), 'message'),
        ('has_large_money_amount', FunctionTransformer(has_large_money_amount, validate=False), 'message'),
        ('has_action_required', FunctionTransformer(has_action_required, validate=False), 'message'),
    ],
    remainder='passthrough'
)

# --- Create a Pipeline ---
# Aumentando n_estimators para melhorar performance com mais features
pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(
        n_estimators=200,  # Aumentado de 100 para 200
        max_depth=30,      # Limita profundidade para evitar overfitting
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1          # Usa todos os cores disponíveis
    ))
])

print("\n" + "="*80)
print("TREINANDO MODELO COM FEATURES AVANÇADAS DE PHISHING + IMPERSONATION")
print("="*80)
print(f"Total de features: 22 (TF-IDF + 4 originais + 12 URL + 6 impersonation)")
print(f"Tamanho do dataset de treino: {len(X_train)} mensagens")
print(f"Tamanho do dataset de teste: {len(X_test)} mensagens")
print(f"Distribuição de classes (treino):")
print(f"  - Ham (não golpe): {sum(y_train == 0)} ({sum(y_train == 0)/len(y_train)*100:.1f}%)")
print(f"  - Spam (golpe): {sum(y_train == 1)} ({sum(y_train == 1)/len(y_train)*100:.1f}%)")
print("\nIniciando treinamento...")

# --- Fit the pipeline ---
pipeline.fit(X_train, y_train)
print("✓ Modelo treinado com sucesso!")

# --- Avaliação ---
print("\nAvaliando modelo no conjunto de teste...")
y_pred = pipeline.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("\n" + "="*80)
print("RESULTADOS DA AVALIAÇÃO")
print("="*80)
print(f"Acurácia: {accuracy:.4f} ({accuracy*100:.2f}%)")

print("\nRelatório Detalhado de Classificação:")
print(classification_report(y_test, y_pred, target_names=['N Golpe (Ham)', 'Golpe (Spam)']))

# Mostrar feature importance (top 20)
print("\n" + "="*80)
print("TOP 20 FEATURES MAIS IMPORTANTES")
print("="*80)
try:
    # Pegar feature names do TF-IDF
    feature_names = []
    tfidf_features = pipeline.named_steps['preprocessor'].named_transformers_['tfidf'].get_feature_names_out()
    feature_names.extend(tfidf_features)

    # Adicionar nomes das features customizadas
    custom_features = [
        'has_url', 'has_phone_number', 'has_money_keywords', 'has_urgency_keywords',
        'num_urls', 'has_ip_url', 'has_shortened_url', 'avg_url_length',
        'has_suspicious_tld', 'max_subdomain_depth', 'has_encoded_chars',
        'has_at_in_url', 'max_hyphens_in_domain', 'has_numbers_in_domain',
        'has_nonstandard_port', 'url_entropy',
        'has_institution_name', 'has_data_request', 'has_prize_claim',
        'has_threat_language', 'has_large_money_amount', 'has_action_required'
    ]
    feature_names.extend(custom_features)

    # Pegar importâncias
    importances = pipeline.named_steps['classifier'].feature_importances_

    # Criar DataFrame e ordenar
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)

    print("\nTop 20 features mais importantes:")
    for idx, row in feature_importance_df.head(20).iterrows():
        print(f"  {row['feature']:<30} {row['importance']:.6f}")

    # Mostrar importância das features customizadas
    print("\n" + "="*80)
    print("IMPORTÂNCIA DAS FEATURES CUSTOMIZADAS")
    print("="*80)
    custom_feature_importance = feature_importance_df[feature_importance_df['feature'].isin(custom_features)]
    for idx, row in custom_feature_importance.iterrows():
        print(f"  {row['feature']:<30} {row['importance']:.6f}")

except Exception as e:
    print(f"Não foi possível calcular feature importance: {e}")


# --- Salvamento do Pipeline ---
print("\n" + "="*80)
print("SALVANDO MODELO")
print("="*80)

if not os.path.exists('models'):
    os.makedirs('models')
    print("✓ Diretório 'models/' criado")

model_path = 'models/pipeline.pkl'
joblib.dump(pipeline, model_path)

print(f"✓ Pipeline salvo em: {model_path}")
print(f"✓ Tamanho do arquivo: {os.path.getsize(model_path) / 1024 / 1024:.2f} MB")
print("\n" + "="*80)
print("TREINAMENTO CONCLUÍDO COM SUCESSO!")
print("="*80)
print("\nPróximos passos:")
print("  1. Execute 'python app.py' para iniciar a API")
print("  2. Teste com: curl -X POST http://localhost:5000/classificar \\")
print("     -H 'Content-Type: application/json' \\")
print("     -d '{\"mensagem\": \"Ganhe iPhone grátis em http://bit.ly/premio\"}'")
print("="*80)

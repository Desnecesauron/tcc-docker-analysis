"""
Script de teste para validar as features avançadas de phishing
"""
import pandas as pd
from features import (
    # Features originais
    has_url, has_phone_number, has_money_keywords, has_urgency_keywords,
    # Features avançadas de URL
    num_urls, has_ip_url, has_shortened_url, avg_url_length,
    has_suspicious_tld, max_subdomain_depth, has_encoded_chars,
    # Features de phishing específicas
    has_at_in_url, max_hyphens_in_domain, has_numbers_in_domain,
    has_nonstandard_port, url_entropy
)

# Mensagens de teste
test_messages = pd.Series([
    "Parabéns! Ganhou iPhone. Clique: http://bit.ly/premio http://malicious.xyz",
    "Urgente! Acesse http://192.168.1.1:8080/phishing",
    "Seu banco: http://banco-secure-login-verify-account.tk/atualizar",
    "Phishing: http://google.com@attacker.com/fake",
    "URL longa: http://site.com/path?param=%3Cscript%3Ealert%281%29%3C%2Fscript%3E",
    "Subdomínio profundo: http://a.b.c.d.example.com/page",
    "Número no domínio: http://paypa1.com/login",
    "Mensagem normal sem links",
    "Ligue para 11987654321 agora!",
    "Ganhe R$ 10.000 hoje mesmo! Última chance!"
])

print("="*80)
print("TESTE DAS FEATURES AVANÇADAS DE PHISHING")
print("="*80)

# Testa cada feature
features_to_test = [
    ("num_urls", num_urls),
    ("has_ip_url", has_ip_url),
    ("has_shortened_url", has_shortened_url),
    ("avg_url_length", avg_url_length),
    ("has_suspicious_tld", has_suspicious_tld),
    ("max_subdomain_depth", max_subdomain_depth),
    ("has_encoded_chars", has_encoded_chars),
    ("has_at_in_url", has_at_in_url),
    ("max_hyphens_in_domain", max_hyphens_in_domain),
    ("has_numbers_in_domain", has_numbers_in_domain),
    ("has_nonstandard_port", has_nonstandard_port),
    ("url_entropy", url_entropy),
]

for feature_name, feature_func in features_to_test:
    print(f"\n{feature_name}:")
    print("-" * 80)
    result = feature_func(test_messages)
    for i, msg in enumerate(test_messages):
        value = result[i][0]
        if isinstance(value, float):
            print(f"  [{value:6.2f}] {msg[:70]}")
        else:
            print(f"  [{value:6}] {msg[:70]}")

print("\n" + "="*80)
print("TESTE DAS FEATURES ORIGINAIS")
print("="*80)

original_features = [
    ("has_url", has_url),
    ("has_phone_number", has_phone_number),
    ("has_money_keywords", has_money_keywords),
    ("has_urgency_keywords", has_urgency_keywords),
]

for feature_name, feature_func in original_features:
    print(f"\n{feature_name}:")
    print("-" * 80)
    result = feature_func(test_messages)
    for i, msg in enumerate(test_messages):
        value = result[i][0]
        print(f"  [{value}] {msg[:70]}")

print("\n" + "="*80)
print("TESTE COMPLETO!")
print("="*80)

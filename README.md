# Classificador de Mensagens de Phishing em Português

## Visão Geral

Este projeto é uma aplicação de machine learning para classificar mensagens de texto em Português do Brasil como "Golpe" ou "Não Golpe", com foco em detecção de phishing e golpes por SMS/WhatsApp.

A aplicação utiliza **RandomForestClassifier** com **22 features customizadas** de engenharia social, análise de URLs e detecção de impersonation, alcançando **94.25% de acurácia**.

## Características Principais

- **Acurácia**: 94.25%
- **Features**: 22 (TF-IDF + 4 básicas + 12 de URL + 6 de impersonation)
- **Dataset**: 1.998 mensagens (v5 - enriquecido com golpes de impersonation)
- **Threshold ajustado**: 40% (maior sensibilidade a golpes)
- **API Endpoints**: v1 (compatibilidade) e v2 (formato estendido)

### Features Implementadas

#### Features Básicas (4)
- Detecção de URLs
- Detecção de números de telefone
- Palavras-chave relacionadas a dinheiro
- Palavras-chave de urgência

#### Features Avançadas de URL (12)
- Número de URLs na mensagem
- URLs com endereço IP
- URLs encurtadas (bit.ly, tinyurl, etc.)
- Comprimento médio de URLs
- TLDs suspeitos (.tk, .ml, .ga, etc.)
- Profundidade de subdomínios
- Caracteres codificados em URLs
- Símbolo @ em URLs
- Hífens em domínios
- Números em domínios
- Portas não padrão
- Entropia de URLs

#### Features de Impersonation e Engenharia Social (6)
- **Nomes de instituições**: ~50 bancos, e-commerce, órgãos públicos
- **Pedidos de dados sensíveis**: cartão, senha, CPF, etc.
- **Promessas de prêmios**: "você ganhou", "foi sorteado"
- **Linguagem de ameaça**: bloqueio, multa, pendência
- **Valores monetários altos**: ≥ R$ 1.000
- **Chamadas para ação**: "clique aqui", "acesse agora"

## Tecnologias Utilizadas

- **Linguagem:** Python 3.9
- **ML/Data Science:** Scikit-learn, Pandas, NLTK
- **Framework Web:** Flask + Flask-CORS
- **Servidor WSGI:** Gunicorn
- **Containerização:** Docker

## Como Executar

### Usando Docker (Recomendado)

A imagem Docker está disponível no Docker Hub:

```bash
# Pull da imagem (477 MB otimizada)
docker pull desnecesauron/classificador-golpes-ptbr

# Executar o container
docker run -p 5000:5000 desnecesauron/classificador-golpes-ptbr
```

**Ou build local:**

```bash
# Build da imagem
docker build -t classificador-golpes-ptbr .

# Executar o container
docker run -p 5000:5000 classificador-golpes-ptbr
```

### Localmente

**Pré-requisitos:**
- Python 3.9 ou superior
- pip

**Instalação e Execução:**

1. **Ative o virtual environment:**
   ```bash
   python3 -m venv venv && source venv/bin/activate
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Treine o modelo:**
   ```bash
   python train_model_v2.py
   ```
   Isso irá:
   - Baixar stopwords do NLTK
   - Treinar o modelo com 22 features
   - Salvar `models/pipeline.pkl` (1.70 MB)
   - Mostrar métricas de avaliação

4. **Execute o servidor da API:**
   ```bash
   python app.py
   ```
   A API estará acessível em `http://localhost:5000`.

## Uso da API

### Endpoints Disponíveis

#### `GET /`
Retorna informações sobre a API.

#### `GET /status`
Retorna status do modelo e pipeline.

#### `POST /classificar` (v1 - Compatibilidade)
Endpoint original com formato simplificado.

**Request:**
```json
{
  "mensagem": "Seu texto aqui"
}
```

**Response:**
```json
{
  "classificacao": "Golpe",
  "confianca": 0.7542
}
```

#### `POST /classificar/v2` (Formato Estendido)
Endpoint com informações detalhadas sobre a classificação.

**Request:**
```json
{
  "mensagem": "Seu texto aqui"
}
```

**Response:**
```json
{
  "classificacao": "Golpe",
  "confianca": 0.7542,
  "nivel_risco": "ALTO",
  "probabilidades": {
    "ham": 0.2458,
    "spam": 0.7542
  },
  "threshold_usado": 0.40,
  "mensagem_analisada": "Seu texto aqui"
}
```

### Níveis de Risco

**Para Golpes:**
- `CRÍTICO`: probabilidade > 80%
- `ALTO`: probabilidade > 60%
- `MÉDIO`: probabilidade > 40%
- `BAIXO`: probabilidade ≤ 40%

**Para Não Golpes:**
- `MUITO SEGURO`: confiança > 90%
- `SEGURO`: confiança > 70%
- `DUVIDOSO`: confiança ≤ 70%

### Exemplos de Uso

**Exemplo com `curl` (v1):**
```bash
curl -X POST http://localhost:5000/classificar \
  -H 'Content-Type: application/json' \
  -d '{"mensagem": "Parabéns! Você ganhou um iPhone 15. Clique aqui: www.premiohoje.com"}'
```

**Exemplo com `curl` (v2):**
```bash
curl -X POST http://localhost:5000/classificar/v2 \
  -H 'Content-Type: application/json' \
  -d '{"mensagem": "Bradesco: Confirme seus dados do cartão para evitar bloqueio"}'
```

**Exemplo com Python:**
```python
import requests

url = "http://localhost:5000/classificar/v2"
payload = {
    "mensagem": "Seu CPF foi premiado com R$ 50.000. Acesse o link para resgatar"
}

response = requests.post(url, json=payload)
print(response.json())
```

## Estrutura do Projeto

```
.
├── app.py                      # API Flask
├── features.py                 # Features customizadas
├── train_model_v2.py          # Script de treinamento
├── requirements.txt           # Dependências
├── Dockerfile                 # Configuração Docker
├── .dockerignore              # Otimização Docker
├── build-and-push-docker.sh   # Script de build/push
├── data/
│   ├── spam_ptbr_v4.tsv      # Dataset v4
│   └── spam_ptbr_v5.tsv      # Dataset v5 (atual)
├── models/
│   └── pipeline.pkl          # Modelo treinado
└── archive/                   # Arquivos de desenvolvimento
    ├── backups/
    ├── documentacao-desenvolvimento/
    ├── resultados-testes/
    └── scripts-desenvolvimento/
```

## Métricas do Modelo

| Métrica | Valor |
|---------|-------|
| **Acurácia** | **94.25%** |
| **Precision (Golpe)** | 98% |
| **Recall (Golpe)** | 79% |
| **F1-Score (Golpe)** | 0.87 |
| **Precision (Não Golpe)** | 93% |
| **Recall (Não Golpe)** | 99% |
| **F1-Score (Não Golpe)** | 0.96 |

### Interpretação
- **98% de precision em golpes**: Quando classifica como golpe, está quase sempre certo
- **79% de recall em golpes**: Detecta 79% dos golpes reais
- **99% de recall em não golpes**: Raramente classifica mensagens legítimas como golpe

## Top 10 Features Mais Importantes

| Rank | Feature | Importância | Tipo |
|------|---------|-------------|------|
| 1 | has_url | 0.1414 | Custom |
| 2 | link (TF-IDF) | 0.0495 | TF-IDF |
| 3 | conta (TF-IDF) | 0.0442 | TF-IDF |
| 4 | has_money_keywords | 0.0320 | Custom |
| 5 | receba (TF-IDF) | 0.0289 | TF-IDF |
| 6 | **has_large_money_amount** | **0.0229** | **Custom (NEW)** |
| 7 | **has_data_request** | **0.0178** | **Custom (NEW)** |
| 8 | grátis (TF-IDF) | 0.0172 | TF-IDF |
| 9 | **has_institution_name** | **0.0166** | **Custom (NEW)** |
| 10 | dados (TF-IDF) | 0.0155 | TF-IDF |

## Evolução do Projeto

- **v1**: Modelo básico com TF-IDF (LogisticRegression)
- **v2**: Adicionadas 4 features customizadas
- **v3**: Adicionadas 12 features de análise de URL
- **v4**: Dataset enriquecido (1.934 mensagens)
- **v5 (atual)**:
  - 6 features de impersonation
  - Dataset v5 com 1.998 mensagens
  - Acurácia: 94.25%
  - Threshold ajustado para 40%

## Build e Deploy

### Script Automatizado

Use o script `build-and-push-docker.sh` para build e push:

```bash
./build-and-push-docker.sh
```

### Manual

```bash
# Build
docker build -t desnecesauron/classificador-golpes-ptbr .

# Push para Docker Hub
docker push desnecesauron/classificador-golpes-ptbr
```

## Documentação Adicional

- [Swagger/OpenAPI](swagger.yaml) - Documentação completa da API
- [MELHORIAS_IMPLEMENTADAS.md](archive/resultados-testes/MELHORIAS_IMPLEMENTADAS.md) - Detalhes das melhorias

## Licença

Este projeto é parte de um TCC (Trabalho de Conclusão de Curso).

## Autor

Desenvolvido como parte do TCC sobre detecção de phishing em mensagens em português.

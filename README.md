# Classificador de Mensagens de Spam em Português

## Visão Geral

Este projeto é uma aplicação de machine learning para classificar mensagens de texto em Português do Brasil como "Golpe" ou "Não Golpe".

A aplicação é composta por dois scripts principais:

1.  `train_model.py`: Treina um modelo de classificação de texto. Ele lê um dataset de mensagens rotuladas, utiliza um `TfidfVectorizer` para converter o texto em features numéricas (removendo stop words em português) e treina um modelo de `LogisticRegression`. O modelo treinado e o vetorizador são salvos no diretório `models/`.
2.  `app.py`: Cria uma API web com Flask. Ele carrega o modelo e o vetorizador pré-treinados e expõe um endpoint `/classificar`. Este endpoint aceita requisições POST com um payload JSON contendo uma mensagem e retorna a classificação (golpe ou não) com um score de confiança.

A aplicação é containerizada usando Docker. O `Dockerfile` configura o ambiente Python, instala as dependências, executa o script de treinamento para gerar os artefatos do modelo e define o comando para rodar a API Flask com `gunicorn`.

## Tecnologias Utilizadas

- **Linguagem:** Python 3.9
- **ML/Data Science:** Scikit-learn, Pandas, NLTK
- **Framework Web:** Flask
- **Servidor WSGI:** Gunicorn
- **Containerização:** Docker

## Como Executar

Existem duas formas de executar o projeto: localmente com Python ou como um container Docker.

### Usando Docker (Recomendado)

O `Dockerfile` automatiza toda a configuração, incluindo o treinamento do modelo.

**Build da imagem:**

```bash
docker build -t tcc-spam-classifier .
```

**Executar o container:**
Este comando inicia a API e mapeia a porta 5000 do container para a porta 5000 do host.

```bash
docker run -p 5000:5000 tcc-spam-classifier
```

### Localmente

**Pré-requisitos:**

- Python 3.9 ou superior
- pip

**Instalação e Execução:**

0.  **Ative o virtual env:**

    ```bash
    python3 -m venv venv && source venv/bin/activate
    ```

1.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Treine o modelo:**
    O script de treinamento irá baixar os dados necessários do NLTK (`stopwords`) e criar o diretório `models/` com os arquivos do modelo e do vetorizador.

    ```bash
    python train_model.py
    ```

3.  **Execute o servidor da API:**
    ```bash
    python app.py
    ```
    A API estará acessível em `http://localhost:5000`.

## Uso da API

Para utilizar o serviço de classificação, envie uma requisição `POST` para o endpoint `/classificar`.

- **URL:** `http://localhost:5000/classificar`
- **Método:** `POST`
- **Headers:** `Content-Type: application/json`
- **Body:**
  ```json
  {
    "mensagem": "Seu texto de mensagem para classificar vai aqui."
  }
  ```

**Exemplo com `curl`:**

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"mensagem": "Parabéns! Você foi selecionado para ganhar um iPhone 15. Clique aqui: www.premiohoje.com"}' \
http://localhost:5000/classificar
```

**Exemplo de Resposta de Sucesso:**

```json
{
  "classificacao": "Golpe",
  "confianca": 0.9987
}
```

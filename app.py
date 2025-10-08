from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd

# Inicializa o aplicativo Flask
app = Flask(__name__)
CORS(app)

# Carrega o modelo e o vetorizador pré-treinados
# Isso acontece apenas uma vez quando o servidor inicia
try:
    model = joblib.load('models/model.pkl')
    vectorizer = joblib.load('models/vectorizer.pkl')
    print("Modelo e vetorizador carregados com sucesso.")
except FileNotFoundError:
    print("Erro: Arquivos de modelo não encontrados. Execute train_model.py primeiro.")
    model = None
    vectorizer = None

@app.route('/')
def home():
    return "API de Classificação de Golpes está no ar. Use o endpoint /classificar."

# Define o endpoint de classificação
@app.route('/classificar', methods=['POST'])
def classificar_mensagem():
    if not model or not vectorizer:
        return jsonify({'error': 'Modelo não está carregado.'}), 500

    # Pega o JSON enviado na requisição
    data = request.get_json()

    # Valida se a chave 'mensagem' existe no JSON
    if not data or 'mensagem' not in data:
        return jsonify({'error': "JSON inválido. A chave 'mensagem' é obrigatória."}), 400

    # Pega o texto da mensagem
    mensagem_texto = data['mensagem']
    
    # Transforma a mensagem em um vetor TF-IDF usando o vetorizador carregado
    mensagem_tfidf = vectorizer.transform([mensagem_texto])

    # Faz a predição (0 ou 1)
    predicao = model.predict(mensagem_tfidf)[0]

    # Calcula a probabilidade de ser golpe (classe 1)
    probabilidades = model.predict_proba(mensagem_tfidf)
    confianca = probabilidades[0][predicao]

    # Formata o resultado
    if predicao == 1:
        classificacao = 'Golpe'
    else:
        classificacao = 'N Golpe (mensagem normal)'

    # Cria a resposta JSON
    resposta = {
        'classificacao': classificacao,
        # Usamos 'confianca' em vez de 'acuracia', pois é a confiança da predição individual
        'confianca': float(f'{confianca:.4f}') 
    }

    return jsonify(resposta)

if __name__ == '__main__':
    # Roda o app. 'host=0.0.0.0' permite acesso externo ao container
    app.run(host='0.0.0.0', port=5000)
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import os
from datetime import datetime

# Inicializa o aplicativo Flask
app = Flask(__name__)
CORS(app)

# Carrega o pipeline pré-treinado
pipeline = None
pipeline_info = {}

try:
    pipeline_path = 'models/pipeline.pkl'
    pipeline = joblib.load(pipeline_path)

    # Informações sobre o pipeline
    file_size = os.path.getsize(pipeline_path) / 1024 / 1024
    pipeline_info = {
        'loaded': True,
        'path': pipeline_path,
        'size_mb': round(file_size, 2),
        'loaded_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    print("="*80)
    print("API DE CLASSIFICAÇÃO DE PHISHING")
    print("="*80)
    print(f"✓ Pipeline carregado com sucesso")
    print(f"  - Arquivo: {pipeline_path}")
    print(f"  - Tamanho: {file_size:.2f} MB")
    print(f"  - Features: TF-IDF + 16 features customizadas")
    print("="*80)

except FileNotFoundError:
    print("="*80)
    print("ERRO: Pipeline não encontrado!")
    print("="*80)
    print("Execute 'python train_model_v2.py' primeiro para treinar o modelo.")
    print("="*80)
    pipeline_info = {'loaded': False, 'error': 'Pipeline file not found'}
except Exception as e:
    print(f"Erro ao carregar pipeline: {e}")
    pipeline_info = {'loaded': False, 'error': str(e)}

@app.route('/')
def home():
    return jsonify({
        'status': 'online',
        'message': 'API de Classificação de Phishing',
        'endpoints': {
            '/': 'Informações da API',
            '/status': 'Status do modelo',
            '/classificar': 'POST - Classifica uma mensagem (formato v1)',
            '/classificar/v2': 'POST - Classifica uma mensagem (formato estendido)'
        },
        'version': '2.0',
        'features': 'TF-IDF + 16 features customizadas'
    })

@app.route('/status')
def status():
    """Retorna informações sobre o status do pipeline"""
    return jsonify({
        'pipeline': pipeline_info,
        'api_status': 'online',
        'ready': pipeline is not None
    })

# Endpoint de classificação V1 (formato original - compatibilidade)
@app.route('/classificar', methods=['POST'])
def classificar_mensagem():
    if not pipeline:
        return jsonify({'error': 'Pipeline não está carregado.'}), 500

    # Pega o JSON enviado na requisição
    data = request.get_json()

    # Valida se a chave 'mensagem' existe no JSON
    if not data or 'mensagem' not in data:
        return jsonify({'error': "JSON inválido. A chave 'mensagem' é obrigatória."}), 400

    # Pega o texto da mensagem
    mensagem_texto = data['mensagem']

    # Validação adicional
    if not isinstance(mensagem_texto, str):
        return jsonify({'error': "A mensagem deve ser uma string"}), 400

    if len(mensagem_texto.strip()) == 0:
        return jsonify({'error': "A mensagem não pode estar vazia"}), 400

    try:
        # Cria um DataFrame com a mensagem
        mensagem_df = pd.DataFrame({'message': [mensagem_texto]})

        # Calcula as probabilidades
        probabilidades = pipeline.predict_proba(mensagem_df)
        prob_spam = probabilidades[0][1]

        # Threshold ajustado: 40% de probabilidade de spam = classifica como golpe
        # Isso torna o modelo mais sensível a golpes (menos falsos negativos)
        THRESHOLD = 0.40

        if prob_spam >= THRESHOLD:
            predicao = 1
            classificacao = 'Golpe'
            confianca = prob_spam
        else:
            predicao = 0
            classificacao = 'N Golpe (mensagem normal)'
            confianca = probabilidades[0][0]

        # Resposta no formato original (v1)
        resposta = {
            'classificacao': classificacao,
            'confianca': float(f'{confianca:.4f}')
        }

        return jsonify(resposta)

    except Exception as e:
        return jsonify({'error': 'Erro ao processar mensagem', 'message': str(e)}), 500


# Endpoint de classificação V2 (formato estendido com mais informações)
@app.route('/classificar/v2', methods=['POST'])
def classificar_mensagem_v2():
    if not pipeline:
        return jsonify({
            'error': 'Pipeline não está carregado.',
            'message': 'Execute train_model_v2.py primeiro'
        }), 500

    # Pega o JSON enviado na requisição
    data = request.get_json()

    # Valida se a chave 'mensagem' existe no JSON
    if not data or 'mensagem' not in data:
        return jsonify({
            'error': "JSON inválido",
            'message': "A chave 'mensagem' é obrigatória",
            'example': {'mensagem': 'Seu texto aqui'}
        }), 400

    # Pega o texto da mensagem
    mensagem_texto = data['mensagem']

    # Validação adicional
    if not isinstance(mensagem_texto, str):
        return jsonify({
            'error': "Tipo inválido",
            'message': "A mensagem deve ser uma string"
        }), 400

    if len(mensagem_texto.strip()) == 0:
        return jsonify({
            'error': "Mensagem vazia",
            'message': "A mensagem não pode estar vazia"
        }), 400

    try:
        # Cria um DataFrame com a mensagem
        mensagem_df = pd.DataFrame({'message': [mensagem_texto]})

        # Calcula as probabilidades
        probabilidades = pipeline.predict_proba(mensagem_df)
        prob_ham = probabilidades[0][0]
        prob_spam = probabilidades[0][1]

        # Threshold ajustado: 40% de probabilidade de spam = classifica como golpe
        THRESHOLD = 0.40

        if prob_spam >= THRESHOLD:
            predicao = 1
            classificacao = 'Golpe'
            confianca = prob_spam
            # Níveis de risco baseados na probabilidade de spam
            if prob_spam > 0.8:
                nivel_risco = 'CRÍTICO'
            elif prob_spam > 0.6:
                nivel_risco = 'ALTO'
            elif prob_spam > 0.4:
                nivel_risco = 'MÉDIO'
            else:
                nivel_risco = 'BAIXO'
        else:
            predicao = 0
            classificacao = 'N Golpe (mensagem normal)'
            confianca = prob_ham
            # Nível de segurança baseado na probabilidade de ham
            if confianca > 0.9:
                nivel_risco = 'MUITO SEGURO'
            elif confianca > 0.7:
                nivel_risco = 'SEGURO'
            else:
                nivel_risco = 'DUVIDOSO'

        # Cria a resposta JSON V2 com informações estendidas
        resposta = {
            'classificacao': classificacao,
            'confianca': round(float(confianca), 4),
            'nivel_risco': nivel_risco,
            'probabilidades': {
                'ham': round(float(prob_ham), 4),
                'spam': round(float(prob_spam), 4)
            },
            'threshold_usado': THRESHOLD,
            'mensagem_analisada': mensagem_texto[:100] + '...' if len(mensagem_texto) > 100 else mensagem_texto
        }

        return jsonify(resposta)

    except Exception as e:
        return jsonify({
            'error': 'Erro ao processar mensagem',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    # Roda o app. 'host=0.0.0.0' permite acesso externo ao container
    if pipeline:
        print("\n" + "="*80)
        print("INICIANDO SERVIDOR DA API")
        print("="*80)
        print("  URL: http://0.0.0.0:5000")
        print("  Endpoints disponíveis:")
        print("    - GET  /              : Informações da API")
        print("    - GET  /status        : Status do modelo")
        print("    - POST /classificar   : Classificar (v1 - compatibilidade)")
        print("    - POST /classificar/v2: Classificar (v2 - formato estendido)")
        print("="*80)
        print("\nPressione CTRL+C para parar o servidor\n")

    app.run(host='0.0.0.0', port=5000, debug=False)
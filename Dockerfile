# 1. Use uma imagem base oficial do Python
FROM python:3.9-slim

# 2. Defina o diretório de trabalho dentro do container
WORKDIR /app

# 3. Copie o arquivo de dependências e instale-as
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copie todos os arquivos do projeto para o diretório de trabalho
COPY . .

# 5. Execute o script de treinamento DURANTE a construção da imagem
RUN python train_model.py

# 6. Exponha a porta que a API usará
EXPOSE 5000

# 7. Defina o comando para rodar a aplicação quando o container iniciar
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

# Imagem base leve com Python 3.12
FROM python:3.12-slim

# Instala dependências de sistema necessárias para:
#   - psycopg2-binary (libpq-dev)
#   - WeasyPrint (instalado via apt para puxar todas as libs nativas automaticamente)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    weasyprint \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia e instala as dependências Python primeiro (para aproveitar o cache de camadas)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY . .

# Expõe a porta usada pelo Flask
EXPOSE 5000

# Comando padrão para iniciar a aplicação
CMD ["python", "app.py"]

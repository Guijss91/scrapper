FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    libgbm1 \
    chromium \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define variáveis de ambiente para o Chrome
ENV CHROME_BIN="/usr/bin/chromium"

# Cria diretório da aplicação
WORKDIR /app

# Copia arquivos
COPY . .

# Instala dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta
EXPOSE 5000

# Executa a aplicação
CMD ["python", "app.py"]

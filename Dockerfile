FROM python:3.11-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    unzip \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libdrm2 \
    libgbm1 \
    libx11-xcb1 \
    libxcb-dri3-0 \
    xdg-utils \
    ca-certificates \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# Instala o Google Chrome (versão estável mais recente)
RUN curl -fsSL https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
 && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update \
 && apt-get install -y google-chrome-stable \
 && rm -rf /var/lib/apt/lists/*

# Define variável de ambiente para o caminho do Chrome
ENV CHROME_BIN="/usr/bin/google-chrome"

# Cria diretório da aplicação
WORKDIR /app

# Copia os arquivos
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expõe a porta 5000 para a API Flask
EXPOSE 5000

# Comando de inicialização
CMD ["python", "app.py"]

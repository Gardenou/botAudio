# Imatge base amb Python
FROM python:3.11-slim

# Instal·lem ffmpeg i dependències del sistema
RUN apt-get update && apt-get install -y ffmpeg && apt-get clean

# Directori de treball
WORKDIR /app

# Copiem els fitxers
COPY . .

# Instal·lem les dependències
RUN pip install --no-cache-dir -r requirements.txt

# Executar el bot
CMD ["python", "main.py"]

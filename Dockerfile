FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY oauth_token_request.py .

EXPOSE 8001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8001", "oauth_token_request:app"]


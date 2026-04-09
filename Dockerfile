FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/scripts/validate_trades.py .
COPY . .
# Run validation script
CMD ["python", "validate_trades.py"]
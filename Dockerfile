FROM python:3.11-slim
WORKDIR /app
# Copy only necessary files
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# Create output directory
RUN mkdir output
# Run validation script
CMD ["python", "validate_trades.py"]
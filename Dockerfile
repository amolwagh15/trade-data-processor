FROM python:3.10-slim
WORKDIR /app
# Copy only necessary files
COPY scripts/validate_trades.py .
COPY source_trade.xml .
# Create output directory
RUN mkdir output
# Run validation script
CMD ["python", "validate_trades.py"]
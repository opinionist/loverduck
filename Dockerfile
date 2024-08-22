FROM python:3.10-slim

WORKDIR /app

COPY request.txt .
RUN pip install --no-cache-dir -r request.txt

COPY loverduck.py .
COPY DateBase.db .

CMD ["python", "loverduck.py"]
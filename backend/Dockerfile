FROM python:3.11-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# El código vive en /app/backend; PYTHONPATH=/app permite `from backend....`
WORKDIR /app
COPY . ./backend/
ENV PYTHONPATH=/app
WORKDIR /app/backend

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
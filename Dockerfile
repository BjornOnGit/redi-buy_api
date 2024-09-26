FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    gobject-introspection
RUN addgroup --system celery && adduser --system --ingroup celery celery
USER celery
COPY . .
COPY .env .env
EXPOSE 8000
ENV ENVIRONMENT=production
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

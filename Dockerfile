# Example Dockerfile snippet
FROM python:3.9

WORKDIR /app/

COPY requirements.txt .
RUN pip install -r requirements.txt

#COPY . .
COPY ./app /app
ENV PYTHONPATH=/app



# Optional: Run migrations during the build
#RUN alembic upgrade head

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


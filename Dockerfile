# Dockerfile

FROM python:3.12

WORKDIR /app

COPY lll.py .

CMD ["python", "lll.py"]

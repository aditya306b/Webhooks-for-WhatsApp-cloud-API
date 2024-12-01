FROM python:3.10.13-alpine3.19

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt

EXPOSE 8000

CMD ["python", "main.py"]

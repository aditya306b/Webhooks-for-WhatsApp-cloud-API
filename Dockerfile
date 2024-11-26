FROM python:3.10.13-alpine3.19

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app
COPY . .

RUN apk add --no-cache bash dos2unix && \
    pip install --no-cache-dir -r ./requirements.txt

# Switch to the non-root user
USER appuser

EXPOSE 8000

CMD ["python", "main.py"]

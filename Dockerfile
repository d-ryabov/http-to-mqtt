FROM python:3 AS builder
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyinstaller
RUN pyinstaller --onefile temp-server.py

FROM python:3-slim
WORKDIR /app
COPY --from=builder /app/dist/temp-server .
EXPOSE 8000/tcp
ENTRYPOINT ["./http-to-mqtt"]

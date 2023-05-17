FROM python:3 AS builder
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install pyinstaller
RUN pyinstaller --onefile http-to-mqtt.py

FROM python:3-slim
WORKDIR /app
COPY --from=builder /app/dist/http-to-mqtt .
ENV HTTP_ADDR=''
ENV HTTP_PORT=8000
EXPOSE 8000/tcp
ENV MQTT_ADDR=127.0.0.1
ENV MQTT_PORT=1883
ENTRYPOINT ["./http-to-mqtt"]

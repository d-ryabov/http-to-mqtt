FROM python:3 AS builder
WORKDIR /app
COPY . .
RUN apk add --no-cache python g++ make
RUN pip install --no-cache-dir -r ./requirements.txt
RUN pip install pyinstaller
RUN pyinstaller --onefile http-to-mqtt.py

FROM python:3-slim
WORKDIR /app
COPY --from=builder /app/dist/http-to-mqtt .
EXPOSE 8000/tcp
ENTRYPOINT ["./http-to-mqtt"]

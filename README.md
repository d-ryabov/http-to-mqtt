# http-to-mqtt
Simple HTTP server for receiving data and then sending to MQTT.

## Installing
There is a multi-arch Docker which supports x86-64, armhf and arm64:
* https://hub.docker.com/r/daryabov/http-to-mqtt/

## Updating
To update your instance, simply re-pull latest image from Docker Hub.

## Configuration
Configuration is carried out through environment variables.

### MQTT_ADDR
*Optional parameter*. This parameter specifies MQTT server address.

**Format:**
```sh
MQTT_ADDR=ip_addr
```

**Default:** `127.0.0.1`

**Example:**
```sh
MQTT_ADDR=192.168.0.1
```

### MQTT_PORT
*Optional parameter*. This parameter specifies MQTT server port.

**Format:**
```sh
MQTT_PORT=ip_port
```

**Default:** `1883`

Example:
```sh
MQTT_PORT=1884
```

### HTTP_ADDR
*Optional parameter*. This parameter specifies HTTP server address.

**Format:**
```sh
HTTP_ADDR=ip_addr
```

**Default:** `''`

**Example:**
```sh
HTTP_ADDR=192.168.0.1
```

### HTTP_PORT
*Optional parameter*. This parameter specifies HTTP server listening port.

**Format:**
```sh
HTTP_PORT=ip_port
```

**Default:** `8000`

Example:
```sh
HTTP_PORT=80
```

## Usage
POST request to `http://<ip_addr>:<ip_port>/api/post/path/to/topic`, which must include JSON of the form: `{"param1": value1, ..., "paramN": valueM}` will send `value1..M` to MQTT topic `/path/to/topic/param1..N`.

Example:
```py
import requests
import json


url = 'http://127.0.0.1:8000/api/post/home/livingroom/'
param = {'temperature': 22, 'humidity': 50}
json_param = json.dumps(param)
resp = requests.post(url, data=json_param)
```

This code will put `22` to `/home/livingroom/temperature` and `50` to `/home/livingroom/humidity`

## Support
Through [GitHub issues](https://github.com/d-ryabov/http-to-mqtt/issues).
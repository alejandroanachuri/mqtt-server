from fastapi import FastAPI, Request
from fastapi_mqtt import FastMQTT, MQQTConfig
import ssl
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

tls_host = os.environ.get('STACKHERO_MOSQUITTO_URL_TLS')
user = os.environ.get('STACKHERO_MOSQUITTO_USER_LOGIN')
passw = os.environ.get('STACKHERO_MOSQUITTO_USER_PASSWORD')

sslSettings = ssl.SSLContext(ssl.PROTOCOL_TLS);
sslSettings.verify_mode = ssl.CERT_NONE;


mqtt_config = MQQTConfig(
    host = 'zzmakp.stackhero-network.com', #"5a4a5fcb82764eae8f9e5db02b9f707c.s1.eu.hivemq.cloud",
    port= 8883,
    username = 'iot-test',
    password = 'Iot-test2022',
    version = 5,
    ssl = sslSettings
    )

mqtt = FastMQTT(
    config=mqtt_config
)

mqtt.init_app(app)

temp = 0

@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("mqtt/temp") #subscribing mqtt topic 
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    global temp
    temp = payload.decode()
    return 0

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)



@app.get("/")
async def func(request: Request):
    return templates.TemplateResponse("index.html",{"request": request, "temp":temp})
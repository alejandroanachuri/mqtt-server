from fastapi import FastAPI
from fastapi_mqtt import FastMQTT, MQQTConfig
import logging
import ssl


app = FastAPI()
log = logging.getLogger("app")
log.setLevel(logging.DEBUG)

sslSettings = ssl.SSLContext(ssl.PROTOCOL_TLS);
sslSettings.verify_mode = ssl.CERT_NONE;

mqtt_config = MQQTConfig(
    host = "5a4a5fcb82764eae8f9e5db02b9f707c.s1.eu.hivemq.cloud",
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


@mqtt.on_connect()
def connect(client, flags, rc, properties):
    mqtt.client.subscribe("/mqtt") #subscribing mqtt topic 
    print("Connected: ", client, flags, rc, properties)

@mqtt.on_message()
async def message(client, topic, payload, qos, properties):
    print("Received message: ",topic, payload.decode(), qos, properties)
    return 0

@mqtt.on_disconnect()
def disconnect(client, packet, exc=None):
    print("Disconnected")

@mqtt.on_subscribe()
def subscribe(client, mid, qos, properties):
    print("subscribed", client, mid, qos, properties)


@app.get("/")
async def func():
    #mqtt.publish("/mqtt", "Hello from Fastapi") #publishing mqtt topic 

    return {"result": True,"message":"Published" }
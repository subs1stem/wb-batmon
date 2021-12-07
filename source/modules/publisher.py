from settings import *
from paho.mqtt.publish import multiple


def publish_meta(name: str, error: str):
    msgs = [
        {'topic': f'{ROOT_MQTT_TOPIC}/meta/name',
         'payload': name,
         'retain': True},

        {'topic': f'{ROOT_MQTT_TOPIC}/meta/error',
         'payload': error,
         'retain': True},
    ]

    multiple(msgs, hostname=MQTT_BROKER_IP)


def publish_control(data,
                    name: str,
                    data_type: str,
                    order: int,
                    error: str,
                    retain=False):
    msgs = [
        {'topic': f'{ROOT_MQTT_TOPIC}/controls/{name}',
         'payload': data,
         'retain': retain},

        {'topic': f'{ROOT_MQTT_TOPIC}/controls/{name}/meta/type',
         'payload': data_type,
         'retain': retain},

        {'topic': f'{ROOT_MQTT_TOPIC}/controls/{name}/meta/order',
         'payload': order,
         'retain': retain},

        {'topic': f'{ROOT_MQTT_TOPIC}/controls/{name}/meta/error',
         'payload': error,
         'retain': retain},
    ]

    multiple(msgs, hostname=MQTT_BROKER_IP)

from os import getenv

from paho.mqtt.publish import multiple


def publish_meta(name: str, error: str):
    msgs = [
        {'topic': '{}/meta/name'.format(getenv('MQTT_ROOT_TOPIC')),
         'payload': name,
         'retain': True},

        {'topic': '{}/meta/error'.format(getenv('MQTT_ROOT_TOPIC')),
         'payload': error,
         'retain': True},
    ]

    multiple(msgs, hostname=getenv('MQTT_BROKER_ADDRESS'))


def publish_control(data,
                    name: str,
                    data_type: str,
                    error: str,
                    order=None,
                    retain=True):
    msgs = [
        {'topic': '{}/controls/{}'.format(getenv('MQTT_ROOT_TOPIC'), name),
         'payload': data,
         'retain': retain},

        {'topic': '{}/controls/{}/meta/type'.format(getenv('MQTT_ROOT_TOPIC'), name),
         'payload': data_type,
         'retain': retain},

        {'topic': '{}/controls/{}/meta/order'.format(getenv('MQTT_ROOT_TOPIC'), name),
         'payload': order,
         'retain': retain},

        {'topic': '{}/controls/{}/meta/error'.format(getenv('MQTT_ROOT_TOPIC'), name),
         'payload': error,
         'retain': retain},
    ]

    multiple(msgs, hostname=getenv('MQTT_BROKER_ADDRESS'))

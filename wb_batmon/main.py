import asyncio
import time
from os import getenv
from statistics import mean

from dotenv import load_dotenv
from requests.exceptions import RequestException

from modules.batmon.batmon import BatMon
from modules.mqtt.mqtt import MQTTClient

load_dotenv()

batmon = BatMon(getenv('BATMON_HOST'))
mqtt_client = MQTTClient(getenv('MQTT_BROKER_HOST'), getenv('MQTT_ROOT_TOPIC'))

mqtt_client.publish_meta(getenv('MQTT_DEVICE_NAME'))

while True:
    try:
        loop = asyncio.get_event_loop()
        slaves_data = loop.run_until_complete(batmon.get_all_data())
        master_data = slaves_data.pop('master_info')

        ip = master_data['ip_address']
        location = master_data['location']
        slaves = master_data['slaves']

        mqtt_client.publish_control(ip, 'IP', 'text')
        mqtt_client.publish_control(location, 'Location', 'text')
        mqtt_client.publish_control(slaves, 'Slaves', 'value')

        if slaves:
            voltages = []
            # publish slaves info
            for slave in range(1, slaves + 1):
                status = slaves_data[slave]['status']
                voltage = slaves_data[slave]['voltage']
                temperature = slaves_data[slave]['temperature']

                if voltage != 0:
                    voltages.append(voltage)

                status_error = voltage_error = temp_error = ''

                if status != 'OK':
                    status_error = 'r'
                    if voltage == 0:
                        voltage_error = 'r'
                    if temperature == -0.06 or temperature == 0 or temperature == 85:
                        temp_error = 'r'

                mqtt_client.publish_control(status, 'SL{}_status'.format(slave), 'text', status_error)
                mqtt_client.publish_control(voltage, 'SL{}_voltage'.format(slave), 'voltage', voltage_error)
                mqtt_client.publish_control(temperature, 'SL{}_temperature'.format(slave), 'temperature', temp_error)

            average_voltage = 0
            if len(voltages) == slaves and len(voltages) != 0:
                average_voltage = round(mean(voltages), 2)

            # publish average voltage
            mqtt_client.publish_control(average_voltage, 'AVG_voltage', 'voltage', '' if average_voltage else 'r')

            # publish voltage deviation
            for slave in range(0, slaves):
                deviation = round(abs(voltages[slave] - average_voltage), 2) if average_voltage else 0

                mqtt_client.publish_control(
                    deviation,
                    'SL{} voltage deviation'.format(slave + 1),
                    'voltage',
                    '' if average_voltage else 'r'
                )

    except RequestException:
        mqtt_client.publish_control(getenv('BATMON_ADDRESS'), 'IP', 'text', 'r')

    finally:
        time.sleep(int(getenv('POLLING_INTERVAL')))

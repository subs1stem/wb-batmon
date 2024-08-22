import asyncio
import time
from statistics import mean

from dotenv import load_dotenv
from requests.exceptions import RequestException

from modules.batmon.batmon import BatMon
from modules.mqtt.mqtt import *

load_dotenv()

batmon = BatMon(getenv('BATMON_ADDRESS'))
publish_meta(name=getenv('MQTT_DEVICE_NAME'), error='')

while True:
    try:
        loop = asyncio.get_event_loop()
        slaves_data = loop.run_until_complete(batmon.get_all_data())
        master_data = slaves_data.pop('master_info')

        # publish master info
        ip = master_data['ip_address']
        location = master_data['location']
        slaves = master_data['slaves']
        publish_control(data=ip,
                        name='IP',
                        data_type='text',
                        # order=1,
                        error='')
        publish_control(data=location,
                        name='Location',
                        data_type='text',
                        # order=2,
                        error='')
        publish_control(data=slaves,
                        name='Slaves',
                        data_type='value',
                        # order=3,
                        error='')

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

                publish_control(data=status,
                                name='SL{}_status'.format(slave),
                                data_type='text',
                                # order=4,
                                error=status_error)
                publish_control(data=voltage,
                                name='SL{}_voltage'.format(slave),
                                data_type='voltage',
                                # order=6,
                                error=voltage_error)
                publish_control(data=temperature,
                                name='SL{}_temperature'.format(slave),
                                data_type='temperature',
                                # order=8,
                                error=temp_error)

            average_voltage = 0
            if len(voltages) == slaves and len(voltages) != 0:
                average_voltage = round(mean(voltages), 2)

            # publish average voltage
            publish_control(data=average_voltage,
                            name='AVG_voltage',
                            data_type='voltage',
                            # order=5,
                            error='' if average_voltage else 'r')

            # publish voltage deviation
            for slave in range(0, slaves):
                deviation = round(abs(voltages[slave] - average_voltage), 2) if average_voltage else 0
                publish_control(data=deviation,
                                name='SL{} voltage deviation'.format(slave + 1),
                                data_type='voltage',
                                # order=7,
                                error='' if average_voltage else 'r')

    except RequestException:
        publish_control(data=getenv('BATMON_ADDRESS'),
                        name='IP',
                        data_type='text',
                        # order=1,
                        error='r')

    finally:
        time.sleep(int(getenv('POLLING_INTERVAL')))

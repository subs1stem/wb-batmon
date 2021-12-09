import asyncio
import time
from statistics import mean

from requests.exceptions import RequestException

from modules.batmon import BatMon
from modules.publisher import *
from settings import *

batmon = BatMon(BATMON_IP)
publish_meta(name=MQTT_CLIENT_NAME, error='')

while True:
    try:
        loop = asyncio.get_event_loop()
        slaves_data = loop.run_until_complete(batmon.get_all_data())
        master_data = slaves_data.pop('master_info')

        #  publish master info
        ip = master_data['ip_address']
        location = master_data['location']
        slaves = master_data['slaves']
        publish_control(data=ip,
                        name='IP',
                        data_type='text',
                        order=1,
                        error='')
        publish_control(data=location,
                        name='Location',
                        data_type='text',
                        order=2,
                        error='')
        publish_control(data=slaves,
                        name='Slaves',
                        data_type='value',
                        order=3,
                        error='')

        if slaves:
            voltages = []
            #  publish slaves info
            for key in slaves_data:
                status = slaves_data[key]['status']
                voltage = slaves_data[key]['voltage']
                temperature = slaves_data[key]['temperature']

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
                                name='SL{} status'.format(key),
                                data_type='text',
                                order=4,
                                error=status_error)
                publish_control(data=voltage,
                                name='SL{} voltage'.format(key),
                                data_type='voltage',
                                order=6,
                                error=voltage_error)
                publish_control(data=temperature,
                                name='SL{} temperature'.format(key),
                                data_type='temperature',
                                order=8,
                                error=temp_error)

            average_voltage = 0
            if len(voltages) == slaves and len(voltages) != 0:
                average_voltage = round(mean(voltages), 2)

            # publish average voltage
            publish_control(data=average_voltage,
                            name='AVG voltage',
                            data_type='voltage',
                            order=5,
                            error='' if average_voltage else 'r')

            # publish voltage deviation
            for slave in range(0, slaves):
                deviation = round(abs(voltages[slave] - average_voltage), 2) if average_voltage else 0
                publish_control(data=deviation,
                                name='SL{} voltage deviation'.format(slave+1),
                                data_type='voltage',
                                order=7,
                                error='' if average_voltage else 'r')

    except RequestException:
        publish_control(data=BATMON_IP,
                        name='IP',
                        data_type='text',
                        order=1,
                        error='r')

    finally:
        time.sleep(POLLING_INTERVAL)
